from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import Profile
from blog.models import Post , Comment



class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username'  , 'password']
        extra_kwargs = {"password":{"write_only":True}}

    def save(self):
        user = User(username=self.validated_data['username'])
        password = self.validated_data['password']
        if (len(password) < 8) or (user.username in password):
            raise serializers.ValidationError({"password":"password must be 8 character or more, username should not be in password"})
        user.set_password(password)
        user.save()
        return user
    


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    new_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_new_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, data):
        user = self.context['user']

        if not user.check_password(data["old_password"]):
            raise serializers.ValidationError({"password":"Incorrect password!"})
        
        if data["new_password"] != data["confirm_new_password"]:
            raise serializers.ValidationError({"confirm_new_password":"Password do not match."})
        
        return data
        


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        extra_kwargs = {
            "user":{ "read_only":True }
        }



class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username" , read_only=True)
    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = {
            'liked_by':{'read_only':True},
            'data_posted':{'read_only':True},
            'author':{'read_only':True},
        }



class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username" , read_only=True)
    related_post_title = serializers.CharField(source="related_post.title" , read_only=True)
    related_post_author = serializers.CharField(source="related_post.author" , read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'related_post':{'read_only':True},
            'author':{'read_only':True},
        }