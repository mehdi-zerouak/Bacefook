from django.urls import path
from .views import Main , postDetail , NewPost , UpdatePost , deletePost

urlpatterns = [
    path('' , Main.as_view() , name='main'),
    path('post/<int:pk>' , postDetail , name='post'),
    path('new-post' , NewPost.as_view() , name='new-post'),
    path('update-post/<int:pk>' , UpdatePost.as_view() , name='update-post'),
    path('delete-post/<int:pk>' , deletePost , name='delete-post' ),
]