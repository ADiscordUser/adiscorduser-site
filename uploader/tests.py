from rest_framework import test, authtoken, reverse, status
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File

from .models import Media
from .serializers import MediaSerializer

import pathlib

class MediaCreationTestCase(test.APITestCase):
    def setUp(self):
        self.client = test.APIClient()
        user = get_user_model().objects.create_user( # type: ignore
            username="creation",
            email="creation@example.com",
            password="test"
        )
        user_auth = authtoken.models.Token.objects.get(user=user) # type: ignore
        self.client.credentials(HTTP_AUTHORIZATION="Token " + user_auth.key)

    def tearDown(self):
        # ensure that the media is deleted from the storage system
        Media.objects.all().delete()

    def verify(self, response):
        # make sure the status code is 201
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # make sure that the media is actually inserted into the db
        inserted_media = Media.objects.get(identifier=response.data["identifier"]) # type: ignore
        serialized = MediaSerializer(inserted_media)
        self.assertEqual(serialized.data, response.data) # type: ignore

    def test_uploads(self):
        """Test media uploads and that its response matches the record in the database."""
        examples = pathlib.Path(f"{settings.MEDIA_ROOT}examples/")
        for example in examples.iterdir():
            with open(example, "rb") as fp:
                f = File(fp, name=example.name)
                r = self.client.post(reverse.reverse("media-list"), {"media": f})
                self.verify(r)

class MediaListTestCase(test.APITestCase):
    def setUp(self):
        self.client = test.APIClient()
        # create multiple users for testing filtered querysets
        self.fake1 = get_user_model().objects.create(
            username="fake1",
            email="fake1@example.com",
            password="test"
        )
        self.fake2 = get_user_model().objects.create(
            username="fake2",
            email="fake2@example.com",
            password="test"
        )
        self.fake1_auth = authtoken.models.Token.objects.get(user=self.fake1).key # type: ignore
        self.fake2_auth = authtoken.models.Token.objects.get(user=self.fake2).key # type: ignore

    def tearDown(self):
        # ensure that the media is deleted from the storage system
        Media.objects.all().delete()

    def test_pagination(self):
        """Tests that pagination specific keys exist."""
        response = self.client.get(reverse.reverse("media-list"), HTTP_AUTHORIZATION="Token " + self.fake1_auth) # it doesn't matter whose token we use

        # check status code
        self.assertEqual(response.status_code, 200)

        # make sure pagination keys are there
        self.assertIn("count", response.data) # type: ignore
        self.assertIn("next", response.data) # type: ignore
        self.assertIn("previous", response.data) # type: ignore
        self.assertIn("results", response.data) # type: ignore

    def test_results_are_from_user(self):
        """Test that the serialized queryset is filtered by the authenticated user."""
        # create media using both users
        with open(f"{settings.MEDIA_ROOT}examples/png.png", "rb") as fp:
            f = File(fp, name="png.png")
            # "fake1" user
            Media.objects.create(media=f, user=self.fake1)
            # "fake2" user
            fp.seek(0)
            Media.objects.create(media=f, user=self.fake2)

        # make request using both users
        fake1_response = self.client.get(reverse.reverse("media-list"), HTTP_AUTHORIZATION="Token " + self.fake1_auth)
        fake2_response = self.client.get(reverse.reverse("media-list"), HTTP_AUTHORIZATION="Token " + self.fake2_auth)

        # check status codes
        self.assertEqual(fake1_response.status_code, 200)
        self.assertEqual(fake2_response.status_code, 200)

        # check "fake1"
        fake1_serialized = MediaSerializer(Media.objects.filter(user=self.fake1), many=True)
        self.assertEqual(fake1_serialized.data, fake1_response.data["results"]) # type: ignore
        # check "fake2"
        fake2_serialized = MediaSerializer(Media.objects.filter(user=self.fake2), many=True)
        self.assertEqual(fake2_serialized.data, fake2_response.data["results"]) # type: ignore

class MediaInstanceTestCase(test.APITestCase):
    def setUp(self):
        self.client = test.APIClient()
        self.user = get_user_model().objects.create_user( # type: ignore
            username="instance",
            email="instance@example.com",
            password="test"
        )
        self.user_auth = authtoken.models.Token.objects.get(user=self.user).key # type: ignore

    def tearDown(self):
        # ensure that the media is deleted from the storage system
        Media.objects.all().delete()

    def test_media_detail(self):
        """Tests getting details (info) on media."""
        with open(f"{settings.MEDIA_ROOT}examples/png.png", "rb") as fp:
            f = File(fp, name="png.png")
            media = Media.objects.create(media=f, user=self.user)

        # fetch media instance using endpoint
        response = self.client.get(reverse.reverse("media-detail", args=[media.identifier]))

        # check status code
        self.assertEqual(response.status_code, 200)

        # make sure that the serialized data from the db matches the response
        serialized = MediaSerializer(media)
        self.assertEqual(serialized.data, response.data) # type: ignore

    def test_media_deletion(self):
        """Test that media is deleted."""
        with open(f"{settings.MEDIA_ROOT}examples/png.png", "rb") as fp:
            f = File(fp, name="png.png")
            media = Media.objects.create(media=f, user=self.user)

        response = self.client.delete(reverse.reverse("media-detail", args=[media.identifier]), HTTP_AUTHORIZATION="Token " + self.user_auth)

        # check status code
        self.assertEqual(response.status_code, 204)

        # make sure that the media doesn't exist anymore
        self.assertFalse(Media.objects.filter(pk=media.identifier).exists())