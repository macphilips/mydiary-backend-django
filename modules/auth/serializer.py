from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserRegistrationSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(required=False, source="first_name")
    lastName = serializers.CharField(required=False, source="last_name")
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(required=False, validators=[
        UniqueValidator(message="Username address already exists", queryset=User.objects.all())])
    email = serializers.CharField(required=False, validators=[
        UniqueValidator(message="Email address already exists", queryset=User.objects.all())])

    class Meta:
        fields = (
            'id',
            'firstName',
            'lastName',
            'email',
            'password',
            'username',
        )
        model = User
