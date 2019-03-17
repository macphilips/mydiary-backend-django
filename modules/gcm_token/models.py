from django.contrib.auth.models import User
from django.db import models

from ..base_model import BaseModel


# Create your models here.

class GcmToken(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)

    class Meta:
        db_table = "gcm_token"
