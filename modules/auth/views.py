from django.contrib.auth.models import User
from django.db.models import Q, QuerySet
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from modules.auth.serializer import UserRegistrationSerializer
from modules.reminder.serializer import ReminderSerializer


@api_view(['POST'])
def save_user(request):
    user_serializer = UserRegistrationSerializer(data=request.data)
    try:
        user_serializer.is_valid(raise_exception=True)

        create_user(user_serializer)

        response = {"status": "True", "message": "Successfully created user entry", "user": user_serializer.data}
        return Response(response, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        errors = user_serializer.errors
        response = {"status": "False", "message": "Validation error", "errors": errors}
        return Response(response, status=e.status_code)


def create_user(user_serializer):
    validated_data = user_serializer.validated_data
    email = validated_data.get('email')
    username = validated_data.get('username', email)
    password = validated_data.get('password')
    first_name = validated_data.get('first_name', "")
    last_name = validated_data.get('last_name', "")
    extra_field = {"first_name": first_name, "last_name": last_name}
    user = User.objects.create_user(username, email, password, **extra_field)
    reminder_serializer = get_reminder_serializer()
    reminder_serializer.is_valid(raise_exception=False)
    reminder_serializer.save(user=user)


def get_reminder_serializer():
    reminder = {
        "time": "12:40",
        "from": "SUNDAY",
        "to": "SATURDAY",
        "enabled": False
    }
    reminder_serializer = ReminderSerializer(data=reminder)
    return reminder_serializer


def validation_email_and_username(email, username):
    errors = {}
    users = User.objects.filter(Q(username=username) | Q(email=email))  # type: QuerySet[User]
    if users.count():
        for user in users:
            if username == user.username:
                errors["username"] = ["Username already exists"]
            if username == user.username:
                errors["email"] = ["Email already exists"]
    return errors
