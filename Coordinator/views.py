from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from App.models import *
from django.contrib import messages
from django.contrib.auth.hashers import check_password,make_password
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.db import IntegrityError
import csv
from django.core.mail import send_mail
# Create your views here.


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
    return render(request,"Coordinator/comments.html",context)

@login_required(login_url="App:loginpage")
def deletePost(request,post_id):
    try:
        post = Post.objects.get(id=post_id)
        if(post.is_event):
            event = Event.objects.get(post=post)
            event.delete()
        # post.delete()
        #the postimage class images are not deleting the while deleting the object of the post so the temporary solution is given here.
        o = PostImage.objects.filter(msg=post_id)
        for i in o:
            i.delete()
        post.delete()
    except:
        pass
        return HttpResponse("Error occured")
    return redirect("Coordinator:dashboard")

@login_required(login_url="App:loginpage")
def myAccount(request):
    pass
    user = request.user
    if(request.method=="POST" or request.FILES):
        pass
        if("firstname" in request.POST):
            firstname = request.POST.get('firstName')
            user.firstName = firstname
            user.save()
        elif("lastname" in request.POST):
            lastname = request.POST.get("lastName")
            user.lastName = lastname
            user.save()
        elif("resetpassword" in request.POST):
            oldpassword = request.POST.get("oldpassword")
            newpassword = request.POST.get("newpassword")
            if(check_password(oldpassword,user.password)):
                user.password=make_password(newpassword)
                user.save()
                logout(request)
                return redirect("App:loginpage")
        elif('changeimage' in request.POST):
            avatar = request.FILES.get("avatar")
            print(avatar)
            user.avatar = avatar
            user.save()
        return redirect("Coordinator:myaccount")
    context={
        "user":user,
    }
    return render(request,"Coordinator/myAccount.html")

@login_required(login_url="App:loginpage")
def deleteavatar(request):
    pass
    user = request.user
    user.avatar = None
    user.save()
    return redirect("Coordinator:myaccount")

@login_required(login_url="App:loginpage")
# Here  admin will upload the pdf of the all the users of the college
def setup(request):
    pass
    users= NewUser.objects.exclude(email="web@gmail.com")
    if(request.method=="POST" or request.FILES):
        if("add by csv" in request.POST):
            pass
            o = Csv(doc = request.FILES.get("doc"))
            o.save()
            with open(o.doc.path,'r') as f:
                reader = csv.reader(f)
                count=0
                for i,row in enumerate(reader):
                    if(i==0):
                        pass
                    else:
                        try:
                            user = NewUser(email = row[0],roll = row[1],firstName=row[2],lastName = row[3])
                            user.save()
                            count+=1
                        except:
                            messages.error(request,"Error occured while creating an user of email "+row[0])
            o.delete()
            if(count!=0):
                messages.success(request,"Total "+str(count)+" users have been created")
            return redirect("Coordinator:setup")
        elif("individual" in request.POST):
            email = request.POST.get("email")
            roll = request.POST.get("roll")
            firstName = request.POST.get("firstname")
            lastName = request.POST.get("lastname")
            isCoordinator = request.POST.get("iscoordinator")
            try:
                if(isCoordinator =="on"):
                    user = NewUser(email = email,roll= roll,firstName=firstName,lastName=lastName,isCoordinator=True)
                else:
                    user = NewUser(email = email,roll= roll,firstName=firstName,lastName=lastName)
                user.save()
                messages.success(request,"The user created successfully")
            except IntegrityError:
                messages.error(request,"The user with email "+email+" already exists")
            finally:
                return redirect("Coordinator:setup")



    return render(request,"Coordinator/setup.html",{"users":users})

def deleteuser(request,id):
    pass
    
    try:
        user = NewUser.objects.get(id=id)
        for i in Post.objects.filter(user=user):
            for j in PostImage.objects.filter(msg=i):
                j.delete()
            i.delete()
        user.delete()
        messages.success(request,"User is deleted")
    except:
        messages.error(request,"Something went wrong please try again")
    return redirect("Coordinator:setup")