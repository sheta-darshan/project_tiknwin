from django import forms
from .models import UserProfile
import re

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio', 'date_of_birth', 'location', 'pan_image', 'aadhar_image']

    # Custom fields for PAN and Aadhar
    pan = forms.CharField(max_length=10, required=True, label="PAN Number")
    aadhar = forms.CharField(max_length=12, required=True, label="Aadhar Number")

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Populate the PAN and Aadhar fields with decrypted values
            self.fields['pan'].initial = self.instance.get_pan()  # Use the decrypt method
            self.fields['aadhar'].initial = self.instance.get_aadhar()  # Use the decrypt method

    def clean_pan(self):
        pan = self.cleaned_data.get('pan')
        if not pan:
            raise forms.ValidationError("PAN is required.")

        # Validate PAN format (e.g., 5 letters, 4 digits, 1 letter)
        if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', pan):
            raise forms.ValidationError("Invalid PAN format. It should be in the format 'ABCDE1234E'.")
        
        # Encrypt and set PAN in the instance
        self.instance.set_pan(pan)
        return pan

    def clean_aadhar(self):
        aadhar = self.cleaned_data.get('aadhar')
        if not aadhar:
            raise forms.ValidationError("Aadhar is required.")

        # Validate Aadhar format (exactly 12 digits)
        if not re.match(r'^\d{12}$', aadhar):
            raise forms.ValidationError("Invalid Aadhar format. It should be a 12-digit number.")
        
        # Encrypt and set Aadhar in the instance
        self.instance.set_aadhar(aadhar)
        return aadhar

    def save(self, commit=True):
        user_profile = super(UserProfileForm, self).save(commit=False)
        # If commit is True, save the profile (this will call the model's save method)
        if commit:
            user_profile.save()
        return user_profile
