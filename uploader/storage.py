from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .validation import get_media_type

import mimetypes

# only implement custom urls for media type specific urls
class MediaStorage(FileSystemStorage):
    def url(self, name):
        identifier = name.split("/")[1]
        # the file name is already based on the correct content type
        # as provided by determine_content_type in models.py
        media_type = get_media_type(mimetypes.guess_type(name)[0]) # type: ignore
        return settings.MEDIA[media_type]["url"] + identifier