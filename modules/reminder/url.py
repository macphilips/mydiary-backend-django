from django.urls import path

from modules.reminder.views import RemindersViewSet

reminder_details = RemindersViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
})

urlpatterns = [
    path('/user/reminder/settings', reminder_details, name='reminders'),
]
