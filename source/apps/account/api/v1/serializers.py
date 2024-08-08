from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

User = get_user_model()


class MobileNumberSerializer(serializers.Serializer):
    mobile_regex = RegexValidator(
        regex=r'09(\d{9})$', message="Enter a valid mobile number. This value may contain only numbers.")
    mobile_number = serializers.CharField(
        max_length=11, validators=[mobile_regex])


class VerifyCodeSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=11)
    code = serializers.CharField(max_length=6)


class CompleteRegistrationSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=11)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=128, write_only=True)

    def create(self, validated_data):
        user = User(
            mobile_number=validated_data['mobile_number'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=11)
    password = serializers.CharField(max_length=128, write_only=True)
