from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from .models import Lomito, Rating, DayTime, NightTime
from .serializers import LomitoSerializer
from .permissions import IsOwnerOrAdmin
from .pagination import CustomPagination


class CustomModelViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny,]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrAdmin,]
        return [permission() for permission in permission_classes]


class LomitosViewSet(CustomModelViewSet):
    serializer_class = LomitoSerializer
    queryset = Lomito.objects.all()
    pagination_class = CustomPagination

    # TODO def retrieve(self, request, pk=None):
    #     queryset = Lomito.objects.all()
    #     lomito = get_object_or_404(queryset, pk=pk)
    #     serializer = LomitoSerializer(lomito)
    #     return Response(serializer.data)
    
    # TODO def update(self, request, *args, **kwargs):
    #     return super().update(request, *args, **kwargs)

    def get_queryset(self):
        params = self.request.query_params

        if not params:
            return super().get_queryset()
        
        params_copy = dict(**params)

        queryset = set()

        data = []

        rating_data = {k: params_copy.pop(k)[0] for k in params.keys() if k == 'rate' or k == 'reviews'}
        rating = Rating.objects.filter(**rating_data)
        data.append(list(rating.values_list('id', flat=True)))

        day_time_data = {k[2::]: params_copy.pop(k)[0] for k in params.keys() if k[0] == 'd'}
        day_time = DayTime.objects.filter(**day_time_data)
        data.append(list(day_time.values_list('id', flat=True)))

        night_time_data = {k[2::]: params_copy.pop(k)[0] for k in params.keys() if k[0] == 'n' and k != 'name'}
        night_time = NightTime.objects.filter(**night_time_data)
        data.append(list(night_time.values_list('id', flat=True)))
        
        rating, day_time, night_time = data
        data = (r for r in rating if r in day_time and r in night_time)

        params_copy = {k: v[0] for k, v in params_copy.items() if k in ['name', 'phone', 'maps', 'logo']}

        for d in data:
            queryset = queryset.union(Lomito.objects.filter(rating=d, day_time=d, night_time=d, **params_copy))

        return list(queryset)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def lomito_base(request):
    rating = list()
    day_time = list()
    night_time = list()
    lomito = list()

    for d in request.data:
        rating.append(d['rating'])
        day_time.append(d['day_time'])
        night_time.append(d['night_time'])
        lomito.append({'name':d['name'], 'phone':d['phone'], 'maps':d['maps'], 'logo':d['logo']})

    Rating.objects.bulk_create([Rating(**r) for r in rating])
    DayTime.objects.bulk_create([DayTime(**d) for d in day_time])
    NightTime.objects.bulk_create([NightTime(**n) for n in night_time])

    rating = Rating.objects.all()
    day_time = DayTime.objects.all()
    night_time = NightTime.objects.all()

    lomitos = [
        Lomito(rating=r, day_time=d, night_time=n, user=request.user,**l) for l, r, d, n in zip(lomito, rating, day_time, night_time)
    ]

    Lomito.objects.bulk_create(lomitos)

    return Response({'success': 'created lomitos'})