from django.db import models
from PIL import Image
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User , on_delete=models.CASCADE , related_name='posts')
    title = models.CharField(max_length=80)
    content = models.CharField(max_length=3000 )
    image = models.ImageField(upload_to='posts-images' , blank=True , null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(User, related_name='likes')

    def __str__(self):
        return f'{self.title} by {self.author.username}'
    
    def save(self):
        super().save()
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 550 or img.width > 550:
                img.thumbnail((500 , 500))
                img.save(self.image.path)

class Comment(models.Model):
    related_post = models.ForeignKey(Post, on_delete=models.CASCADE , related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE , related_name='comments')
    comment = models.CharField(max_length=5500)

    def __str__(self):
        return f'{self.author} comment on {self.related_post}'
    