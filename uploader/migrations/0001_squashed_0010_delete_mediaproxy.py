# Generated by Django 3.0.7 on 2020-07-04 04:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uploader.models


class Migration(migrations.Migration):

    replaces = [('uploader', '0001_initial'), ('uploader', '0002_auto_20200627_2251'), ('uploader', '0003_auto_20200628_1615'), ('uploader', '0004_auto_20200630_0058'), ('uploader', '0005_auto_20200630_0102'), ('uploader', '0006_media_media_type'), ('uploader', '0007_auto_20200701_0157'), ('uploader', '0008_auto_20200701_0220'), ('uploader', '0009_mediaproxy'), ('uploader', '0010_delete_mediaproxy')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('identifier', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('custom_identifier', models.BooleanField()),
                ('hash', models.TextField()),
                ('media', models.FileField(upload_to=uploader.models.determine_media_path)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('media_type', models.CharField(blank=True, default=1, max_length=5)),
            ],
            options={
                'permissions': [('custom_identifiers', 'Can have custom identifiers')],
            },
        ),
        migrations.CreateModel(
            name='MediaProxy',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('uploader.media',),
        ),
        migrations.DeleteModel(
            name='MediaProxy',
        ),
    ]
