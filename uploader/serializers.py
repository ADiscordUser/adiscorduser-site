from rest_framework import serializers

from .models import Media
from core.serializers import UserSerializer

class MediaSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    url = serializers.FileField(source="media", read_only=True)

    class Meta:
        model = Media
        fields = "__all__"
        extra_kwargs = {
            "media": {"write_only": True},
            "media_type": {"read_only": True},
            "identifier": {"read_only": True},
            "custom_identifier": {"read_only": True},
            "hash": {"read_only": True}
        }