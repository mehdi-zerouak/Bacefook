from django.contrib import admin
from django.urls import path , include
from users import urls as users_urls
from blog import urls as blog_urls
from API import urls as API_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/' , include(API_urls)),
    path('' , include(users_urls)),
    path('' , include(blog_urls)),
]
