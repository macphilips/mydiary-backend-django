from django.core.validators import RegexValidator
from rest_framework import serializers

from modules.account.serializer import OwnerSerializer
from modules.reminder.models import Reminder


class ReminderSerializer(serializers.ModelSerializer):
    daysOfTheWeek = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']
    time_validator = RegexValidator(regex='^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$',
                                    message='Invalid time format: HH:mm:ss', )

    time = serializers.CharField(max_length=8, min_length=5, validators=[time_validator], source="md_time")
    user = OwnerSerializer(read_only=True)

    def validate_from(self, value):
        if value.upper() not in self.daysOfTheWeek:
            raise serializers.ValidationError('Field is not a valid a day of the week');
        return value.upper()

    def validate_to(self, attrs):
        return self.validate_from(attrs)

    class Meta:
        fields = (
            'id',
            'user',
            'time',
            'from',
            'to',
            'enabled',
        )
        model = Reminder
        extra_kwargs = {'from': {'source': 'from_date'}, 'to': {'source': 'to_date'}, 'time': {'source': 'md_time'}}
