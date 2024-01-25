from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def get_routes(request):
    site = 'https://' if request.is_secure() else 'http://' + get_current_site(request).domain
    
    routes = {'Lomitos': f'{site}/api/lomitos/','Authentication': f'{site}/api/auth/'}
    
    return Response(routes)


def home(request):
    return redirect('routes')