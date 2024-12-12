from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from .models import UserProfile
import re

class UserProfileForm(forms.ModelForm):
    # Custom fields for PAN, Aadhar, and Email
    pan = forms.CharField(max_length=10, required=True, label="PAN Number")
    aadhar = forms.CharField(max_length=12, required=True, label="Aadhar Number")
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio', 'date_of_birth', 'location', 'pan_image', 'aadhar_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Populate initial values for fields
        if self.instance and self.instance.pk:
            self.fields['pan'].initial = self.instance.get_pan()  # Decrypted PAN
            self.fields['aadhar'].initial = self.instance.get_aadhar()  # Decrypted Aadhar
            self.fields['email'].initial = self.instance.user.email  # User's email
            
        # Make image fields optional
            self.fields['profile_picture'].required = False
            self.fields['pan_image'].required = False
            self.fields['aadhar_image'].required = False

    def validate_and_encrypt(self, field_name, value, pattern, error_message, setter):
        """
        Validates the value using a regex pattern, encrypts it, and sets it using the provided setter method.
        """
        if not value:
            raise forms.ValidationError(f"{field_name} is required.")

        if not re.match(pattern, value):
            raise forms.ValidationError(error_message)

        # Encrypt and set the value using the model's setter method
        setter(value)
        return value

    def clean_pan(self):
        pan = self.cleaned_data.get('pan')
        return self.validate_and_encrypt(
            field_name='pan',
            value=pan,
            pattern=r'^[A-Z]{3}P[A-Z][0-9]{4}[A-Z]$',
            error_message="Invalid PAN format. It should be in the format 'ABCPE1234E'.",
            setter=self.instance.set_pan
        )

    def clean_aadhar(self):
        aadhar = self.cleaned_data.get('aadhar')
        return self.validate_and_encrypt(
            field_name='aadhar',
            value=aadhar,
            pattern=r'^\d{12}$',
            error_message="Invalid Aadhar format. It should be a 12-digit number.",
            setter=self.instance.set_aadhar
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Ensure email is unique across users, excluding the current instance's user
        if UserProfile.objects.exclude(user=self.instance.user).filter(user__email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth:
            today = date.today()
            age = today.year - date_of_birth.year - (
                (today.month, today.day) < (date_of_birth.month, date_of_birth.day)
            )
            if age < 18:
                raise ValidationError("You must be at least 18 years old to register.")
        return date_of_birth

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        # Update the associated User instance's email
        user_profile.user.email = self.cleaned_data['email']

        if commit:
            user_profile.save()
            user_profile.user.save()

        return user_profile
