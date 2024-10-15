from django.views.generic import UpdateView, DetailView
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class UserProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = "profiles/profile_detail.html"

    def get_object(self, queryset=None):
        return self.request.user.userprofile


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'profiles/edit_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user.userprofile

    def get_success_url(self):
        # Redirect to the profile view after successful update
        return self.success_url  # This can also simply return self.success_url since it's already defined
    
    def form_valid(self, form):
        # Update the email field of the related User instance
        self.request.user.email = form.cleaned_data.get('email')
        self.request.user.save()
        return super().form_valid(form)
