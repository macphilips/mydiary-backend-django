from django.urls import path

from modules.entries.views import EntriesViewSet

entries = EntriesViewSet.as_view({
    'post': 'create',
    'get': 'list',
})
entries_details = EntriesViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy',
    'put': 'update'
})
urlpatterns = [
    path('', entries, name='entries'),
    path('/<int:pk>', entries_details, name='entry-details'),
]
