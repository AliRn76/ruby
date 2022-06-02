from django.contrib.auth.hashers import make_password

from user.exceptions import UsernameOrPasswordIsNotCorrect
from user.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, attrs):
        attrs['password'] = make_password(attrs['password'])
        return attrs

    def to_representation(self, instance):
        return {}


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3, max_length=15, allow_null=False)
    password = serializers.CharField(min_length=4, max_length=15, allow_null=False)

    def validate_username(self, username):
        try:
            self.user = User.objects.get(username=username)
            return username
        except User.DoesNotExist:
            raise UsernameOrPasswordIsNotCorrect

    def validate_password(self, password):
        if not self.user.check_password(password):
            raise UsernameOrPasswordIsNotCorrect
        return password


class ProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ReadOnlyField(source='get_profile_picture')
    class Meta:
        model = User
        exclude = ('password', 'is_banned', 'is_staff')
        read_only = ('date_joined', 'last_login', 'phone_number')
        extra_kwargs = {
            'username': {'required': False},
        }


class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('profile_picture', )

    def to_representation(self, instance):
        return {'profile_picture': instance.get_profile_picture}
