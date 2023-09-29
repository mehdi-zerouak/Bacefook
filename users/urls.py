from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from .views import login , Register , profileP , profileC , UpdateProfile , ChangePassword

urlpatterns = [
    path('login/' , login.as_view() , name='login'),
    path('logout/' , LogoutView.as_view(next_page='login') , name='logout'),
    path('register/' , Register.as_view() , name='register'),
    path('profile/<str:user_name>' , profileP , name='profile'),
    path('profile/comments/<str:user_name>' , profileC , name='profile-C'),
    path('update-profile/<int:pk>' , UpdateProfile.as_view() , name='update-profile'),
    path('change-password/' , ChangePassword , name='change-password')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)