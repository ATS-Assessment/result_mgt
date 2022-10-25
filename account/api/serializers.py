from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
# User = get_user_model()
from ..models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('full_name', 'password', 'password2', 'email')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            full_name=validated_data['full_name'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class UserLoginSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': _("Invalid credential")
    }

    @classmethod
    def get_token(cls, user):
        print(user)
        token = super().get_token(user)
        token['email'] = user.email
        token['is_superuser'] = user.is_superuser
        token['full_name'] = user.full_name
        token['is_staff'] = user.is_staff

        return token


class EducatorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('full_name', 'username', 'email')
