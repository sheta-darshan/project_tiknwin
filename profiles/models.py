from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
import base64
import os
from django.core.validators import RegexValidator
from django.utils.text import slugify

# Ensure the environment variable is loaded correctly
ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')

if ENCRYPTION_KEY is None:
    raise ValueError("ENCRYPTION_KEY environment variable is not set.")

# Create a Fernet cipher instance
cipher = Fernet(ENCRYPTION_KEY.encode())  # Use encode() here since ENCRYPTION_KEY is a string

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)

    # PAN and Aadhar fields with validators
    encrypted_pan = models.CharField(max_length=255, blank=True, null=True)
    encrypted_aadhar = models.CharField(max_length=255, blank=True, null=True)

    # To store images of PAN and Aadhar
    pan_image = models.ImageField(upload_to='pan_images/', null=True, blank=True)
    aadhar_image = models.ImageField(upload_to='aadhar_images/', null=True, blank=True)

    # Validators for PAN and Aadhar
    pan_validator = RegexValidator(regex=r'^[A-Z]{5}[0-9]{4}[A-Z]$', message="PAN must be in the format ABCDE1234E.")
    aadhar_validator = RegexValidator(regex=r'^\d{12}$', message="Aadhar must be a 12-digit number.")

    def __str__(self):
        return self.user.username

    # Encryption and Decryption methods
    def encrypt_data(self, data):
        if data:
            return cipher.encrypt(data.encode()).decode()
        return None

    def decrypt_data(self, encrypted_data):
        if encrypted_data:
            decrypted_data = cipher.decrypt(encrypted_data)
            return decrypted_data.decode()
        return None

    # Save method to automatically encrypt PAN and Aadhar before saving
    def save(self, *args, **kwargs):
        # Change the image filenames based on the user information
        if self.profile_picture:
            # Use slugify to make username URL-safe and add user ID for uniqueness
            self.profile_picture.name = f"profile_pics/{slugify(self.user.username)}_{self.user.id}_profile.jpg"
        if self.pan_image:
            # Add user ID to PAN image filename
            self.pan_image.name = f"pan_images/{slugify(self.user.username)}_{self.user.id}_pan.jpg"
        if self.aadhar_image:
            # Add user ID to Aadhar image filename
            self.aadhar_image.name = f"aadhar_images/{slugify(self.user.username)}_{self.user.id}_aadhar.jpg"

        super(UserProfile, self).save(*args, **kwargs)

    # Methods to set and get decrypted PAN and Aadhar for better security
    def set_pan(self, pan):
        self.pan_validator(pan)  # Validate PAN before setting
        self.encrypted_pan = self.encrypt_data(pan)

    def get_pan(self):
        return self.decrypt_data(self.encrypted_pan)

    def set_aadhar(self, aadhar):
        self.aadhar_validator(aadhar)  # Validate Aadhar before setting
        self.encrypted_aadhar = self.encrypt_data(aadhar)

    def get_aadhar(self):
        return self.decrypt_data(self.encrypted_aadhar)
