from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models as db
from django.utils.translation import gettext_lazy as _

from ..base_model import BaseModel


def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(
            _('%(value)s is not an even number'),
            params={'value': value},
        )


# Create your models here.

class Reminder(BaseModel):
    user = db.OneToOneField(User, related_name="reminder", on_delete=db.CASCADE)
    md_time = db.CharField(max_length=8)
    from_date = db.CharField(max_length=10)
    to_date = db.CharField(max_length=10)
    enabled = db.BooleanField(default=False)

    class Meta:
        db_table = "reminders"
