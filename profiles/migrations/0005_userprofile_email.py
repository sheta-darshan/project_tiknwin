# Generated by Django 5.1.2 on 2024-10-15 03:31

import builtins
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_alter_userprofile_aadhar_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(blank=True, null=True, unique=True),
            preserve_default=False,
        ),
    ]
