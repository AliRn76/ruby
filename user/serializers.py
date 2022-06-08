from django.contrib.auth.hashers import make_password

from cache.queries import set_otp, get_forget_password_otp, remove_forget_password_otp
from configs.messages import SUCCESS_OTP
from configs.settings import OTP_LEN, OTP_EXP_SECOND
from user.exceptions import UsernameOrPasswordIsNotCorrect, OTPIsNotValid, UsernameAlreadyExists
from user.models import User, UserRoom
from rest_framework import serializers

from user.utils import generate_otp


class UsernameSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3, max_length=15, allow_null=False)


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, attrs):
        attrs['password'] = make_password(attrs['password'])
        return attrs

    def to_representation(self, instance):
        return {}


class LoginSerializer(UsernameSerializer):
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


class CheckUsernameSerializer(UsernameSerializer):
    def validate_username(self, username):
        try:
            User.objects.get(username=username)
            raise UsernameAlreadyExists
        except User.DoesNotExist:
            return username


class SubmitPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number']
        extra_kwargs = {
            'phone_number': {'required': True}
        }

    def update(self, instance, validated_data):
        # TODO: Send OTP
        set_otp(user_id=self.context['request'].user.id, otp=generate_otp())
        return super(SubmitPhoneSerializer, self).update(instance, validated_data)

    def to_representation(self, instance):
        return {'detail': SUCCESS_OTP, 'timer': OTP_EXP_SECOND}


class SubmitOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(min_length=OTP_LEN, max_length=OTP_LEN, allow_null=False)


class NewPasswordSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(min_length=OTP_LEN, max_length=OTP_LEN, allow_null=False)

    class Meta:
        model = User
        fields = ['password', 'otp']

    def validate_otp(self, otp):
        _otp = get_forget_password_otp(user_id=self.context['request'].user.id)
        if otp == _otp:
            remove_forget_password_otp(user_id=self.context['request'].user.id)
            return otp
        else:
            raise OTPIsNotValid


class ProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ReadOnlyField(source='get_profile_picture')

    class Meta:
        model = User
        exclude = ('password', 'is_banned', 'is_staff')
        read_only_fields = ('date_joined', 'last_login', 'phone_number')
        extra_kwargs = {
            'username': {'required': False},
        }


class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('profile_picture', )

    def to_representation(self, instance):
        return {'profile_picture': instance.get_profile_picture}


class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoom
        exclude = ('user_id', )
        read_only_fields = ('is_pv', 'room_id', 'last_message', 'timestamp')


class ContactSerializer(serializers.Serializer):
    phone_number = serializers.CharField(min_length=11, max_length=15)
