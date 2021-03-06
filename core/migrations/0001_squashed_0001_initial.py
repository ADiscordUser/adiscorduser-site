# Generated by Django 3.1.3 on 2020-11-25 21:23

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('core', '0001_initial')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=20, unique=True, validators=[django.core.validators.MinLengthValidator(3)])),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('gender', models.CharField(choices=[('Normal', (('male', 'Male'), ('female', 'Female'))), ('Other', (('unknown', 'Prefer not to say'), ('mtf', 'Male to Female'), ('ftm', 'Female to Male'), ('binary', 'Binary'), ('nonbinary', 'Non-Binary'), ('genderfluid', 'Genderfluid'), ('agender', 'Agender'), ('bigender', 'Bigender'), ('polygender', 'Polygender'), ('neutrois', 'Neutrois'), ('gender_apathetic', 'Gender Apathetic'), ('androgyne', 'Androgyne'), ('intergender', 'Intergender'), ('demigender', 'Demigender'), ('greygender', 'Greygender'), ('aporagender', 'Aporagender'), ('attack_helicopter', 'Attack Helicopter'), ('dishwasher', 'Dishwasher'), ('maverique', 'Maverique'), ('novigender', 'Novigender'), ('designated_gender', 'Designated gender'), ('afab', 'Assigned Female at Birth'), ('amab', 'Assigned Male at Birth'), ('gender_roles', 'Gender roles'), ('gender_presentation', 'Gender presentation'), ('transitioning', 'Transitioning'), ('intersex', 'Intersex'), ('dyadic', 'Dyadic'), ('trans_woman', 'Transgender Woman'), ('trans_man', 'Transgender Man'), ('trans_feminine', 'Transgender Feminine'), ('trans_masculine', 'Transgender Masculine'), ('social_dysphoria', 'Social Dysphoria'), ('body_dysphoria', 'Body Dysphoria'), ('butch', 'Butch'), ('femme', 'Femme (Fem)'), ('binarism', 'Binarism')))], max_length=69)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_key', models.TextField(editable=False, null=True, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': [('custom_identifiers', 'Can have custom identifiers')],
            },
        ),
    ]
