from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from .serializers import *
# Create your views here.
def loginpage(request):
    if(request.user.is_authenticated):
        pass
        user = request.user
        if(user.isCoordinator==False):
            return redirect("App:dashboard")
        else:
            return redirect("Coordinator:dashboard")
    else:

        if(request.method=="POST"):
            email = request.POST.get("email")
            password = request.POST.get("password")
            user = authenticate(email=email, password=password)
            print(email)
            print(password)
            print(user)
            if (user is not None):
                login(request,user)
                if(user.isCoordinator==False):
                    return redirect("App:dashboard")
                else:
                    return redirect("Coordinator:dashboard")
            else:
                messages.error(
                        request, " email or password are wrong please try again")
                return redirect("App:loginpage")
        return render(request,"App/loginpage.html")

@login_required(login_url="App:loginpage")
def logoutuser(request):
    pass
    logout(request)
    return redirect("App:loginpage")

@login_required(login_url="App:loginpage")
def signUp(request):
    if(request.method=="POST"):
        email = request.POST.get("email")
        roll = request.POST.get("roll")
        fn = request.POST.get("fn")
        ln = request.POST.get("ln")
        password = request.POST.get("password")
        try:
            user = NewUser(email=email,roll=roll,firstName = fn,lastName=ln,password = make_password(password))
            user.save()
            return redirect("App:loginpage")
        except:
            print("Something went wrong")
        
    return render(request,"App/signup.html")

@login_required(login_url="App:loginpage")
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
        else:
            messages.error(request,"Post can't be empty")
        return redirect("App:dashboard")
    context = {
        "user":user,
        "posts":posts 
    }
    return render(request,"App/dashboard.html",context)

@login_required(login_url="App:loginpage")
def like(request):
    user = request.user
    if(request.POST.get("action")=="post"):
        pass
        liked=False
        post_id = int(request.POST.get("postid"))
        post = Post.objects.get(id=post_id)
        if(post.likes.filter(id=user.id).exists()):
            post.likes.remove(user)
            post.like_counter -= 1
            liked=False
            post.save()
        else:
            post.likes.add(user)
            post.like_counter+=1
            liked=True
            post.save()
        result=str(post.like_counter)
        return JsonResponse({"result":result,"liked":liked})

@login_required(login_url="App:loginpage")
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
    return render(request,"App/comments.html",context)


@api_view(['GET'])
def get_comments(request,id):
    pass
    try:
        post = Post.objects.get(id=id)
    except:
        pass
    comments = Comment.objects.filter(msg=post)
    serializer = CommentSerializer(comments,many=True)
    return Response(serializer.data)

@login_required(login_url="App:loginpage")
def deleteavatar(request):
    pass
    