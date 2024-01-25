from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.serializers import ValidationError

from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site

from .serializers import MyTokenObtainPairSerializer, SignupSerializer, ChangePasswordEmailSerializer, ChangePasswordSerializer
from .utils import account_activation_token, send_email

from rest_framework_simplejwt.views import TokenObtainPairView


@api_view(['GET'])
def get_routes(request):
    site = 'https://' if request.is_secure() else 'http://' + request.get_host

    routes = {
        'Signup': f'{site}/api/auth/signup/',
        'Login': f'{site}/api/auth/login/',
        'Change Password': f'{site}/api/auth/change-password/',
        'User info': f'{site}/api/auth/user/',
        'Refresh token': f'{site}/api/auth/token/refresh/',
    }

    return Response(routes)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class SignupAPIView(CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [AllowAny,]

    def create(self, request, *args, **kwargs):
        try:
            if request.data['password'] != request.data['repeat_password']:
                raise ValidationError({'password': 'passwords do not match.'})
        except KeyError as err:
            raise ValidationError({str(err).replace("'", ""): 'enter a valid value.'})
        
        serializer = SignupSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=200, data=serializer.data)


class UserInformationAPIVIew(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        user = request.user
        email = user.email
        created_at = user.created_at
        payload = {'id': user.pk, 'email': email, 'created_at': created_at}
        return Response(data=payload, status=200)


def get_user_with_token(uidb64):
    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    return user


def activate(request, uidb64, token):
    user = get_user_with_token(uidb64)

    if user and account_activation_token.check_token(user, token):
        user.is_email_confirmed = True
        user.save()

        return JsonResponse({"Success": "Thank you for your email confirmation. Now you can login your account."})
    else:
        return JsonResponse({"Error": "Activation link is invalid!"})


class ChangePasswordEmailView(CreateAPIView):
    serializer_class = ChangePasswordEmailSerializer
    permission_classes = [AllowAny,]

    def post(self, request, *args, **kwargs):
        User = get_user_model()

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data.get('email')

        if not User.objects.filter(email=email).exists():
            raise ValidationError({'Email': f'This email {email} is not registered.'})
        user = User.objects.get(email=email)

        subject='Change your password'
        msg='change your password:'
        view='users:change_password'

        send_email_confirm = send_email(request, user, email, subject=subject, msg=msg, view=view)
        if send_email_confirm:
            raise ValidationError({'Email': f'Problem sending email to {email}, check if you typed correctly.'})

        return Response(status=200, data={'Success': 'Check your email to change your password!'})


class ChangePasswordView(CreateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [AllowAny,]

    def post(self, request, *args, **kwargs):
        user = get_user_with_token(kwargs['uidb64'])

        if user and account_activation_token.check_token(user, kwargs['token']):
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            user.set_password(request.data.get('new_password'))
            user.save()

            return JsonResponse({"Success": "Password changed!. Now you can login your account."})
        else:
            return JsonResponse({"Error": "Activation link is invalid!"})