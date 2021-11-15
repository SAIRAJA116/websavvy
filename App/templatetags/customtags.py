from django import template
from App.models import *

register = template.Library()

@register.simple_tag
def getImages(msg_id):
    images = PostImage.objects.filter(msg=msg_id)
    return images

@register.simple_tag
def isliked(post_id,user_id):
    post = Post.objects.get(id=post_id)
    if(post.likes.filter(id=user_id).exists()):
        return True
    else:
        return False