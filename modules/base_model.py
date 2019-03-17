from django.db import models
from rest_framework import serializers


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(BaseModel, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        abstract = True
        ordering = ('created_date',)


class BaseModelSerializer(serializers.ModelSerializer):
    createdDate = serializers.DateTimeField(read_only=True, source="created_date")
    lastModified = serializers.DateTimeField(read_only=True, source="modified_date")

    class Meta:
        fields = (
            'createdDate',
            'lastModified',
        )
        model = BaseModel
        abstract = True
