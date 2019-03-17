# Create your views here.
from django.core.handlers import exception
from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import ValidationError, APIException
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from modules.entries import models, serializer as serializers
from permissions.owner_read_only import IsOwner


class EntryPaginator(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'size'


class EntriesViewSet(viewsets.GenericViewSet):
    queryset = models.Entry.objects.all()
    serializer_class = serializers.EntrySerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    pagination_class = EntryPaginator

    def retrieve(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            response = {"status": "True", "message": "Successfully retrieved entry", "entry": serializer.data}
            return Response(response, status=status.HTTP_200_OK)
        except ValidationError as e:
            response = {"status": "False", "message": "Validation error", "errors": serializer.errors}
            return Response(response, status=e.status_code)
        except APIException as e:
            response = {"status": "False", "message": e.default_detail}
            return Response(response, status=e.status_code)
        except exception.Http404:
            response = {"status": "False", "message": "Entry not found"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=request.user)
            response = {"status": "True", "message": "Successfully created user entry", "entry": serializer.data}
            return Response(response, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            response = {"status": "False", "message": "Validation error", "errors": serializer.errors}
            return Response(response, status=e.status_code)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            partial = kwargs.pop('partial', True)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = {"status": "True", "message": "Successfully created user entry", "entry": serializer.data}
            return Response(response, status=status.HTTP_200_OK)
        except ValidationError as e:
            response = {"status": "False", "message": "Validation error", "errors": serializer.errors}
            return Response(response, status=e.status_code)

        except APIException as e:
            response = {"status": "False", "message": e.default_detail}
            return Response(response, status=e.status_code)

        except exception.Http404:
            response = {"status": "False", "message": "Entry not found"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request):
        try:
            self.get_object().delete()
            response = {"status": "True", "message": "Successfully Deleted Entry"}
            return Response(response, status=status.HTTP_200_OK)
        except APIException as e:
            response = {"status": "False", "message": e.default_detail}
            return Response(response, status=e.status_code)
        except exception.Http404:
            response = {"status": "False", "message": "Entry not found"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(models.Entry.objects.filter(owner=request.user))
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            response = {"status": "True", "message": "Successfully Deleted Entry", "entries": serializer.data}
            return Response(response, status=status.HTTP_200_OK)
        except APIException as e:
            response = {"status": "False", "message": e.default_detail}
            return Response(response, status=e.status_code)
        except exception.Http404:
            response = {"status": "False", "message": "Entry not found"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
