from django.contrib.auth.models import User
from django.db import models as db

from ..base_model import BaseModel


# Create your models here.

class Entry(BaseModel):
    title = db.CharField(max_length=200)
    content = db.TextField(null=False)
    owner = db.ForeignKey(User, related_name='entries', on_delete=db.CASCADE)

    class Meta:
        db_table = "entries"
