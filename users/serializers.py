from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .utils import send_email

User = get_user_model()


class ChangePasswordEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email',)


class ChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    repeat_new_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ('new_password', 'repeat_new_password')

    def validate(self, attrs):
        if attrs.get('new_password') != attrs.get('repeat_new_password'):
            raise serializers.ValidationError({'password': 'passwords do not match'})
        
        return attrs


class SignupSerializer(serializers.ModelSerializer):
    repeat_password = serializers.CharField(required=True, write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'repeat_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True}
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('repeat_password')

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(email=validated_data['email'], password=validated_data['password'])

        try:
            validate_password(password=validated_data['password'], user=user)
        except ValidationError as err:
            user.delete()
            raise serializers.ValidationError({'password': err.messages})
        
        subject='Activate your user account.'
        msg='confirm your registration:'
        view='users:activate'
        
        send_email_confirm = send_email(self.context['request'], user, user.email, subject=subject, msg=msg, view=view)
        if send_email_confirm:
            raise serializers.ValidationError({'Email': f'Problem sending email to {user.email}, check if you typed correctly.'})
        
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        if user.is_email_confirmed:
            token = super().get_token(user)
            token['email'] = user.email
            return token
        raise serializers.ValidationError({'Email Confirm': 'Please confirm your email address. Note: Check spam!'}) 