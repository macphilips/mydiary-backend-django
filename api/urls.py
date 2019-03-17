from django.urls import path, include

urlpatterns = (
    path('auth', include('modules.auth.url')),
    path('account', include('modules.account.url')),
    path('entries', include('modules.entries.url')),
    path('account', include('modules.reminder.url')),
    path('authenticate/', include('rest_framework.urls')),
)
