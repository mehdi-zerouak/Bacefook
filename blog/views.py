from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render , redirect
from .models import Post , Comment
from .forms import CommentForm , PostForm
from django.views.generic import ListView , DetailView , CreateView , UpdateView , DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.

class Main(LoginRequiredMixin , ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/main.html'
    login_url = 'login'
    ordering = ['-date_posted']


#post detail + comment form
@login_required
def postDetail(request , pk):
    post = Post.objects.get(id=pk)

    if request.method == 'POST':
        comment = Comment()
        new_comment = request.POST['comment']
        comment.comment = new_comment
        comment.author = request.user
        comment.related_post = post
        comment.save()
        return redirect('post' , pk=post.id)

    context = {'post':post , 'commentForm':CommentForm , 'comments':Comment.objects.filter(related_post=post)}
    return render(request , 'blog/post.html' , context)


class NewPost(LoginRequiredMixin , CreateView):
    model = Post
    template_name = 'blog/new-post.html'
    form_class = PostForm

    def form_valid(self, form):
        post = form.save(commit=False)   
        post.author = self.request.user
        post.save()
        return HttpResponseRedirect(reverse_lazy('main'))
    
class UpdatePost(LoginRequiredMixin , UpdateView):
    model = Post
    template_name = 'blog/update-post.html'
    form_class = PostForm
    success_url = reverse_lazy('main')

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

@login_required   
def deletePost(request , pk):
    user_posts = Post.objects.filter(author=request.user)
    post = user_posts.get(id=pk)
    post.delete()
    return redirect('main')