# Create your views here.
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from modules.account import serializer
from modules.account.serializer import UserSerializer
from modules.gcm_token.models import GcmToken
from permissions.owner_read_only import IsOwner

from rest_framework import serializers


class RegisterGCMSerializer(serializers.Serializer):
    gcmToken = serializers.CharField(write_only=True)


class ChangePasswordSerializer(serializers.Serializer):
    oldPassword = serializers.CharField(write_only=True, min_length=8, max_length=128)
    newPassword = serializers.CharField(write_only=True, min_length=8, max_length=128)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializer.UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    @action(detail=True, url_path="/me")
    def current_login_user(self, request, *args, **kwargs):
        return JsonResponse(UserSerializer(request.user).data)

    @action(detail=True, url_path="/register-token")
    def register_gcm_token(self, request, *args, **kwargs):
        user = request.user
        gcm = RegisterGCMSerializer(data=request.data)
        if gcm.is_valid():
            try:
                gcm_token = GcmToken.objects.get(user=user)
            except GcmToken.DoesNotExist:
                gcm_token = GcmToken(token=gcm.validated_data.get("gcmToken"), user=user)
            gcm_token.save()
            return Response({"status": "Successful", "message": "Saved token"}, status=status.HTTP_200_OK)
        return Response(self.validation_error_json(gcm.errors), status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, url_path="/register-tokens")
    def delete_gcm_token(self, request, *args, **kwargs):
        user = request.user
        try:
            GcmToken.objects.get(user=user).delete()
            return Response({"status": "Successful", "message": "Removed user token"}, status=status.HTTP_200_OK)
        except GcmToken.DoesNotExist:
            return Response({"status": "Failed", "message": "Token does not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, url_path="/change-password")
    def change_password(self, request):
        change = ChangePasswordSerializer(data=request.data)
        if change.is_valid():
            user = request.user
            if user.check_password(change.validated_data.get("oldPassword")):
                user.set_password(change.validated_data.get("newPassword"))
                user.save()
                return Response({"status": "Successful", "message": "Password updated"}, status=status.HTTP_200_OK)
            return Response({"status": "Failed", "message": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(self.validation_error_json(change.errors), status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def validation_error_json(errors):
        return {"status": "Failed", "message": "Validation errors", "errors": errors}
