from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from modules.account.views import UsersViewSet

update_user_account = UsersViewSet.as_view({
    'post': 'update',
})
current_login_user = UsersViewSet.as_view({
    'get': 'current_login_user'
})
change_password = UsersViewSet.as_view({
    'post': 'change_password'
})
register_token = UsersViewSet.as_view({
    'post': 'register_gcm_token',
    'delete': 'delete_gcm_token'
})
urlpatterns = format_suffix_patterns([
    path('', update_user_account, name='update-user'),
    path('/me', current_login_user, name='me'),
    path('/me/detailed', current_login_user, name='me-details'),
    path('/change-password', change_password, name='change-password'),
    path('/register-token', register_token, name='register-token')
])
