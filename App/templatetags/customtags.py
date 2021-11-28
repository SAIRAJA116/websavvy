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

@register.simple_tag
def getevent(post_id):
    event = Event.objects.get(post=post_id)
    return event

@register.simple_tag
def getnoofpost(user_id):
    post = Post.objects.filter(user=user_id).count()
    return post