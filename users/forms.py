from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio", "pfp")
        widgets = {
            'bio':forms.Textarea(attrs={'rows':10, 'cols':70})
            }
