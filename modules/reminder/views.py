# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from modules.reminder.models import Reminder
from modules.reminder.serializer import ReminderSerializer
from permissions.owner_read_only import IsOwner


class RemindersViewSet(viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def update(self, request):
        reminder = self.get_user_reminder(request.user)
        serialize = ReminderSerializer(data=request.data)
        if not reminder:
            reminder = Reminder()
            reminder.user = request.user

        if serialize.is_valid():
            reminder.md_time = serialize.validated_data.get("md_time", reminder.md_time)
            reminder.from_date = serialize.validated_data.get("from_date", reminder.md_time)
            reminder.to_date = serialize.validated_data.get("to_date", reminder.md_time)
            reminder.enabled = serialize.validated_data.get("enabled", reminder.md_time)
            reminder.save()
            return Response(
                {"reminder": serialize.data, "message": "Successfully updated reminder settings", "status": "True"},
                status=status.HTTP_200_OK)

        return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request):
        reminder = self.get_user_reminder(request.user)
        if reminder:
            data = ReminderSerializer(reminder).data
            message = "Retrieved reminder settings"
            return Response({"reminder": data, "message": message, "status": "Successful"}, status=status.HTTP_200_OK)
        else:
            message = "Can't find settings for this user"
            return Response({"message": message, "status": "False"}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def get_user_reminder(user):
        try:
            reminder = Reminder.objects.get(user=user)
        except Reminder.DoesNotExist:
            reminder = None
        return reminder
