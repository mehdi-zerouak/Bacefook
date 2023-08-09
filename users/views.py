from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView 
from .models import Profile


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
    
def profile(request , user_name):
    _user = User.objects.get(username=user_name)
    profile = Profile.objects.get(user=_user)
    return render(request , 'users/profile.html' , {'profile':profile})