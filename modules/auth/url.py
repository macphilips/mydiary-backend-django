from django.urls import path
from rest_framework_jwt.views import (obtain_jwt_token, refresh_jwt_token, verify_jwt_token)

from modules.account.views import UsersViewSet
from modules.auth.views import save_user

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
urlpatterns = [
    path('/signup', save_user, name='sign-up'),
    path('/login', obtain_jwt_token, name='token_obtain_pair'),
    path('/login/refresh', refresh_jwt_token, name='token_refresh'),
    path('/login/verify', verify_jwt_token, name='token_verify'),
]
