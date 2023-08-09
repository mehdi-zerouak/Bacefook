from django import forms
from .models import Post

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 70, 'maxlength': 5500}))
    
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title' , 'content' , 'image')
        widgets = {
          'content': forms.Textarea(attrs={'rows':10, 'cols':70}),
        }
