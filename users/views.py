from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView  , UpdateView
from .models import Profile
from .forms import ProfileForm


# Create your views here.

class login(LoginView):
    template_name = 'users/form.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('main')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context
    
class Register(CreateView):
    template_name = 'users/form.html'
    model = User
    form_class = UserCreationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register'
        return context
    
    #to create a profile when a new user is created instead of using signals
    def form_valid(self, form):
        new_user = form.save()
        user_profile = Profile()
        user_profile.user = new_user
        user_profile.save()
        return HttpResponseRedirect(reverse_lazy('login'))
    
#profile and user posts
def profileP(request , user_name):
    _user = User.objects.get(username=user_name)
    profile = Profile.objects.get(user=_user)
    user_posts = _user.posts.all()
    return render(request , 'users/profile.html' , {'profile':profile , 'user_posts':user_posts})

#profile and user comments
def profileC(request , user_name):
    _user = User.objects.get(username=user_name)
    profile = Profile.objects.get(user=_user)
    user_comments = _user.comments.all()
    return render(request , 'users/profileC.html' , {'profile':profile , 'user_comments':user_comments})

class UpdateProfile(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'users/update-profile.html'

    def get_success_url(self):
        profile_id = self.kwargs['pk']
        profile = Profile.objects.get(id=profile_id)
        user_name = profile.user.username
        return reverse_lazy('profile' , kwargs={'user_name':user_name})

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)