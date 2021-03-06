from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include

from uploader.views import MediaViewSet

api_router = DefaultRouter(trailing_slash=False)
api_router.register("media", MediaViewSet, basename="media")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_router.urls)),
    path("", include("core.urls"))
]