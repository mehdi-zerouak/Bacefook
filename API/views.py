from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView , RetrieveUpdateDestroyAPIView , ListAPIView , CreateAPIView 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK , HTTP_400_BAD_REQUEST , HTTP_201_CREATED
from django.shortcuts import get_object_or_404
#costum permissions
from .permissions import isOwnerOrReadOnly_Profile , isOwnerOrReadOnly_Post
#serializers
from .serializers import (
    UserRegistrationSerializer , ProfileSerializer ,
    PostSerializer , CommentSerializer , ChangePasswordSerializer )
#models
from users.models import Profile 
from blog.models import Post , Comment
from django.contrib.auth.models import User

# Create your views here.

#blacklist token view - logout
class BlacklistToken(APIView):
    def post(self , request):
        try:
            token = request.data['refresh']
            refresh_token = RefreshToken(token)
            refresh_token.blacklist()
            return Response({'message':'refresh token blacklisted!'} , status=HTTP_200_OK)
        except Exception:
            return Response({'error':'token not found or already blacklisted'} , status=HTTP_400_BAD_REQUEST)
        

#create new user
class Register(APIView):
    def post(self , request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            #create a profile for the new user (instead of using signals)
            profile = Profile(user=user)
            profile.save()
            return Response({"user":"user registred successfully!"} , status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    

#_____________User__________________________________________

class UserProfile(RetrieveUpdateAPIView):
    permission_classes = [isOwnerOrReadOnly_Profile, IsAuthenticated]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    lookup_field = 'user__username'




class ChangeUserPassword(APIView):
    permission_classes = [IsAuthenticated]
    def put(self , request):
        user = self.request.user
        serializer = ChangePasswordSerializer(data=request.data , context={"user":user})

        if serializer.is_valid():
            new_password = request.data['new_password']
            user.set_password(new_password)
            user.save()
            return Response({"password":"password changed successfully."} , status=HTTP_200_OK)
        else:
            return Response(serializer.errors , status=HTTP_400_BAD_REQUEST)


class UserPosts(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        user = User.objects.get(username=self.kwargs['username'])
        return Post.objects.filter(author=user).order_by('-date_posted')



class UserComments(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        user = User.objects.get(username=self.kwargs['username'])
        return Comment.objects.filter(author=user)
    


#_____________Blog__________________________________________

#main
class BlogPosts(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('-date_posted')



class CreatePost(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user) 



class PostDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated , isOwnerOrReadOnly_Post]
    serializer_class = PostSerializer
    queryset = Post.objects.all()



class PostComments(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(related_post=post_id)
    


class CommentDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated , isOwnerOrReadOnly_Post]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()



class CreateComment(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        author = self.request.user
        post_id = self.kwargs['post_id']
        related_post = get_object_or_404(Post, pk=post_id)
        serializer.save(related_post=related_post , author=author)



class LikeOrDislikePost(APIView):
    permission_classes = [IsAuthenticated]
    def post(self , request, *args , **kwargs):
        user = self.request.user
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post , pk=post_id)

        if post.liked_by.filter(id=user.id).exists():
            post.liked_by.remove(user)
            return Response({"message":"u disliked the post"})
        else:
            post.liked_by.add(user)
            return Response({"message":"u liked the post"})