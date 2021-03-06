from django.conf import settings

from rest_framework.validators import ValidationError
from rest_framework.exceptions import UnsupportedMediaType

import magic

from django.core.files import uploadedfile, File
from typing import Union

def get_media_type(content_type: str) -> str:
    for item in settings.MEDIA.items(): # get media types in a list and iterate through each media type
        if content_type in item[1]["mime_types"]: # find the mime type provided in one of the media types
            return item[0]
    # if the media type wasn't found, let the user know that the media type isn't supported
    raise UnsupportedMediaType(content_type)

def _validate_media(instance: Union[uploadedfile.UploadedFile, File]):
    mime_type = magic.from_buffer(instance.read(2048), mime=True)
    if mime_type != instance.content_type: # type: ignore , this is provided by the manager for the Media model
        raise ValidationError("The media did not match the specified media type.")

def media_type_validator(instance: Union[uploadedfile.UploadedFile, File]):
    # if the media type provided by the client is not a valid one, an error will be raised here
    get_media_type(instance.content_type) # type: ignore
    # _validate_media only checks to make sure that the media is of the type provided
    # by the client
    _validate_media(instance)