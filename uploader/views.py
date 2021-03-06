from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.filters import OrderingFilter

from rest_framework.exceptions import PermissionDenied
from .serializers import MediaSerializer
from .models import Media
from .signals import clear_cf_cache

import copy

class MediaViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin, mixins.ListModelMixin,
                    GenericViewSet):
    serializer_class = MediaSerializer
    lookup_value_regex = "[^/]+" # make sure file extensions (.) aren't matched

    filter_backends = [OrderingFilter]
    ordering_fields = ["identifier", "custom_identifier", "media_type", "created_at", "hash"]
    ordering = "-created_at"

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.user != self.request.user and not self.request.user.is_superuser: # type: ignore
            raise PermissionDenied("You must be the owner of the media to delete the media.")

        mc = copy.copy(instance)
        instance.delete()
        clear_cf_cache.send(self.__class__, request=self.request, instance=mc)

    def get_queryset(self):
        if self.action == "list":
            # only return media that the user created when listing
            queryset = Media.objects.filter(user=self.request.user)
        else:
            queryset = Media.objects.all()
        return queryset

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]