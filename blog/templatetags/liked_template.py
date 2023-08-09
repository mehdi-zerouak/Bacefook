from django import template

register = template.Library()

@register.filter(name='liked')
def liked(post, user):
    return post.liked_by.filter(id=user.id).exists()