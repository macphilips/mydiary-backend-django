from rest_framework import serializers

from modules.gcm_token.models import GcmToken


class GcmTokenSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'user',
            'token',
        )
        model = GcmToken
