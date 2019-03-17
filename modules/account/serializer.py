from django.contrib.auth.models import User
from rest_framework import serializers


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'username',
            'email',
        )
        model = User


class EntrySerializer(serializers.Serializer):
    count = serializers.SerializerMethodField()
    lastModified = serializers.SerializerMethodField()

    def get_count(self, obj):
        return obj.count()

    def get_lastModified(self, obj):
        entries = obj.order_by('-modified_date')
        return entries[0].modified_date if len(entries) else None


class UserSerializer(serializers.ModelSerializer):
    entry = EntrySerializer(read_only=True, source="entries")
    reminder = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('id', 'username', 'entry', 'reminder')
