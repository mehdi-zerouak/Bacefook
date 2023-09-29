from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio", "pfp")
        widgets = {
            'bio':forms.Textarea(attrs={'rows':10, 'cols':70})
            }

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=60 , widget=forms.PasswordInput())
    new_password = forms.CharField(max_length=60 , widget=forms.PasswordInput())
    confirm_new_password = forms.CharField(max_length=60 , widget=forms.PasswordInput())