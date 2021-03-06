from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver

from .storage import MediaStorage
from . import validation

import mimetypes
import pathlib
import string
import random
import hashlib
import magic

def determine_media_path(instance: "Media", filename: str) -> str:
    media_type = validation.get_media_type(instance.content_type) # type: ignore , this is provided by the manager
    return f"{media_type}/{instance.identifier}"

class MediaManager(models.Manager):
    def create(self, *args, **kwargs):
        if hasattr(kwargs.get("media"), "content_type"):
            # an uploaded file
            self.model.content_type = kwargs.get("media").content_type
        else:
            # a regular django.core.files.File instance
            self.model.content_type = magic.from_buffer(kwargs.get("media").file.read(2048), mime=True)
        return super(MediaManager, self).create(*args, **kwargs)

class Media(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    identifier = models.SlugField(max_length=30, blank=True, primary_key=True)
    custom_identifier = models.BooleanField()
    hash = models.TextField()
    media = models.FileField(upload_to=determine_media_path, validators=[validation.media_type_validator], storage=MediaStorage)
    media_type = models.TextField(choices=[("image", "Image"), ("video", "Video")])
    created_at = models.DateTimeField(auto_now_add=True)

    objects = MediaManager()

    def save(self, *args, **kwargs):
        self.custom_identifier = bool(self.identifier)
        self.hash = hashlib.sha512(self.media.file.read()).hexdigest()
        self.media_type = validation.get_media_type(self.content_type) # type: ignore

        if not self.identifier:
            extension = mimetypes.guess_extension(self.content_type) # type: ignore
            self.identifier = self.generate_identifier() + extension # type: ignore

        return super(Media, self).save(*args, **kwargs)

    def generate_identifier(self) -> str:
        characters = random.choices(
            string.ascii_letters + string.digits,
            k=7
        )
        return "".join(characters)

    def __str__(self) -> str:
        return self.identifier

    class Meta:
        verbose_name_plural = "media"
        permissions = [("custom_identifiers", "Can have custom identifiers")]

@receiver(models.signals.post_delete, sender=Media)
def remove_from_storage(sender, instance, **kwargs):
    if instance.media:
        # missing_ok=True allows us to delete a file from the filesystem
        # and then later remove it from the database
        pathlib.Path(instance.media.path).unlink(missing_ok=True)