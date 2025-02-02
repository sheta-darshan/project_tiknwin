# Generated by Django 5.1.2 on 2024-10-14 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='aadhar_image',
            field=models.ImageField(blank=True, null=True, upload_to='aadhar_images/'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='encrypted_aadhar',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='encrypted_pan',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='pan_image',
            field=models.ImageField(blank=True, null=True, upload_to='pan_images/'),
        ),
    ]
