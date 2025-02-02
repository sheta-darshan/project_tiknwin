# Generated by Django 5.1.2 on 2024-10-15 03:50

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_alter_userprofile_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(default=django.utils.timezone.now, max_length=254, unique=True),
            preserve_default=False,
        ),
    ]
