from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView
from . import views

urlpatterns = [
    #authentication
    path('token/' , TokenObtainPairView.as_view() , name='token-view'),
    path('token/refresh/' , TokenRefreshView.as_view() , name='token-refresh-view'),
    #blacklist token - logout
    path('token/blacklist/' , views.BlacklistToken.as_view() , name='blacklist-token'),
    #registration
    path('register/' , views.Register.as_view() , name='register'),
    #user______
    path('user/change-password/' , views.ChangeUserPassword.as_view() , name='change-password'),
    path('profile/<str:user__username>/' , views.UserProfile.as_view() , name='profiles'),
    path('profile/<str:username>/posts/' , views.UserPosts.as_view() , name='user-posts'),
    path('profile/<str:username>/comments/' , views.UserComments.as_view() , name='user-comments'),
    #blog______
    path('', views.BlogPosts.as_view() , name='blog-posts'),
    path('new-post/' , views.CreatePost.as_view() , name='create-post'),
    path('post/<int:pk>/' , views.PostDetail.as_view() , name='post-detal'),
    path('post/<int:post_id>/comments/' , views.PostComments.as_view() , name='post-comments'),
    path('post/<int:post_id>/like-dislike/' , views.LikeOrDislikePost.as_view() , name='like-post'),
    path('post/<int:post_id>/new-comment/' , views.CreateComment.as_view() , name='new-comment'),
    path('comment/<int:pk>/' , views.CommentDetail.as_view() , name='comment-detail'),
]