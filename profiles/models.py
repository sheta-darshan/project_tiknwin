from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
import os
from django.core.validators import RegexValidator
import uuid
from datetime import datetime

# Load encryption key from environment
ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')
if ENCRYPTION_KEY is None:
    raise ValueError("ENCRYPTION_KEY environment variable is not set.")

# Create a Fernet cipher instance
cipher = Fernet(ENCRYPTION_KEY.encode())

def profile_pic_upload_to(instance, filename):
    """Generates a file path for profile picture uploads."""
    ext = filename.split('.')[-1]
    return f'profile_pics/{instance.user.id}_{uuid.uuid4().hex}.{ext}'

def pan_upload_to(instance, filename):
    """Generates a file path for PAN card image uploads."""
    ext = filename.split('.')[-1]
    return f'pan_images/{instance.user.id}_{uuid.uuid4().hex}.{ext}'

def aadhar_upload_to(instance, filename):
    """Generates a file path for Aadhar card image uploads."""
    ext = filename.split('.')[-1]
    return f'aadhar_images/{instance.user.id}_{uuid.uuid4().hex}.{ext}'

class UserProfile(models.Model):
    MEMBERSHIP_CHOICES = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to=profile_pic_upload_to, null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    points = models.PositiveIntegerField(default=0)
    membership_type = models.CharField(max_length=10, choices=MEMBERSHIP_CHOICES, default='basic', editable=False)

    encrypted_pan = models.CharField(max_length=255, blank=True, null=True)
    encrypted_aadhar = models.CharField(max_length=255, blank=True, null=True)
    pan_image = models.ImageField(upload_to=pan_upload_to, null=True, blank=True)
    aadhar_image = models.ImageField(upload_to=aadhar_upload_to, null=True, blank=True)

    pan_validator = RegexValidator(regex=r'^[A-Z]{3}P[A-Z][0-9]{4}[A-Z]$', message="PAN must be in the format ABCPE1234E.")
    aadhar_validator = RegexValidator(regex=r'^\d{12}$', message="Aadhar must be a 12-digit number.")

    def __str__(self):
        return self.user.username
    
    def get_email(self):
        return self.user.email

    # Encryption and Decryption methods
    def encrypt_data(self, data):
        if data:
            return cipher.encrypt(data.encode()).decode()
        return None

    def decrypt_data(self, encrypted_data):
        if encrypted_data:
            return cipher.decrypt(encrypted_data.encode()).decode()
        return None

    # Methods to set and get decrypted PAN and Aadhar for better security
    def set_pan(self, pan):
        self.pan_validator(pan)
        self.encrypted_pan = self.encrypt_data(pan)

    def get_pan(self):
        return self.decrypt_data(self.encrypted_pan)

    def set_aadhar(self, aadhar):
        self.aadhar_validator(aadhar)
        self.encrypted_aadhar = self.encrypt_data(aadhar)

    def get_aadhar(self):
        return self.decrypt_data(self.encrypted_aadhar)

    # Update membership type based on points
    def update_membership_type(self):
        if self.points >= 1000:
            self.membership_type = 'premium'
        else:
            self.membership_type = 'basic'

    def add_points(self, amount):
        self.points += amount
        self.save()

    def reset_points(self):
        self.points = 0
        self.save()
