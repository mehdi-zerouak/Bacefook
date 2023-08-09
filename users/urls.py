from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from .views import login , Register , profile

urlpatterns = [
    path('login/' , login.as_view() , name='login'),
    path('logout/' , LogoutView.as_view(next_page='login') , name='logout'),
    path('register/' , Register.as_view() , name='register'),
    path('profile/<str:user_name>' , profile , name='profile')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)