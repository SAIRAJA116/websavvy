from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from App.models import *
from django.contrib import messages
# Create your views here.


def dashboard(request):
    user = request.user
    posts = Post.objects.all()
    if(request.method=="POST" or request.FILES):
        
        message = request.POST.get("message")
        images = request.FILES.getlist("images")
        url = request.POST.get("url")
        if(len(message)!=0 or (url is not None) or len(images)!=0):
            if(len(images)==0):
                post = Post(user = user,message=message,url=url)
            else:
                post = Post(user = user,message=message,url=url,image=images[0])
            post.save()
            if(len(images)>1):
                for i in range(1,len(images)):
                    obj = PostImage(msg=post,image=images[i])
                    obj.save()
            print(request.POST.get("postorevent")) 
            if(request.POST.get("postorevent") == "event"):
                print("in")
                title = request.POST.get("title")
                if(title!=""):
                    post.is_event=True
                    post.save()
                    event = Event(title = title,post = post)
                    event.save()
                else:
                    post.delete()
                    messages.error(request,"Event title can't be empty")
        else:
            messages.error(request,"Post can't be empty")
        
        return redirect("Coordinator:dashboard")
    context = {
        "user":user,
        "posts":posts 
    }
    return render(request,"Coordinator/dashboard.html",context)


def comments(request,id):
    pass
    try:
        post=Post.objects.get(id=id)
    except:
        return HttpResponse("Something went wrong")
    user=request.user
    comments = Comment.objects.filter(msg=post)
    if(request.method == "POST"):
        message = request.POST.get("message")
        print(message)
        print(type(message))
        if(len(message)!=0):
            comment = Comment(msg = post,user = user,comment = message)
            comment.save()
            return JsonResponse({"result":"success"})
        else:
            messages.error(request,"Post can't be empty")
        
    context = {
        "user":user,
        "post":post,
        "comments":comments
        }
    return render(request,"Coordinator/comments.html",context)

def deletePost(request,post_id):
    try:
        post = Post.objects.get(id=post_id)
        if(post.is_event):
            event = Event.objects.get(post=post)
            event.delete()
        post.delete()
    except:
        pass
        return HttpResponse("Error occured")
    return redirect("Coordinator:dashboard")