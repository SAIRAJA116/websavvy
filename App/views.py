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
from django.core.mail import send_mail
import random

#dependies required for HTML email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string #This is used for convert the html in to sharable string format
from django.utils.html import strip_tags
#################################

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



def forgotpassword(request):
    if(request.user.is_authenticated):
        pass
        user = request.user
        if(user.isCoordinator==False):
            return redirect("App:dashboard")
        else:
            return redirect("Coordinator:dashboard")
    else:
        if(request.method == "POST"):
            email = request.POST.get("email")
            try:
                user = NewUser.objects.get(email=email)
                otp = make_password(generateOTP(user.email,user.get_fullname()))
                print(type(otp))
                print(otp)
                o = OTPContainer(otp = otp)
                o.save()
                return redirect("App:validateotp",email=email,otp=str(o.id))
            except:
                pass
                messages.error(request,"User with this email address does not exits, please make sure wheather you are using valid email or not")
        return render(request,"App/forgotpassword.html")


def generateOTP(email,name):
    series = "0123456789"
    otp = "".join(random.sample(series,6))
    # -----------------Sending OTP to Email ---------------------

    # body = '''
    # Dear {name},
    # Here is you OTP:  {otp}    
    # '''.format(name=name,otp=otp)
    # send_mail("Support",body,"websavvy.info@gmail.com",[email],fail_silently=False)

    #creating the html email
    html_content = render_to_string("App/OTP.html",{"name":name,"otp":otp})
    text_content = strip_tags(html_content)
    email_obj=EmailMultiAlternatives(
        #subject
        "Websavvy Support",
        #content
        text_content,
        #from email
        "websavvy.info@gmail.com",
        #to email
        [email]
    )
    email_obj.attach_alternative(html_content,"text/html")
    email_obj.send()
    # -----------------------------------------------------------
    return otp


def validateOTP(request,email,otp):
    pass
    if(request.method == "POST"):
        pass
        userotp = request.POST.get("otp")
        password = request.POST.get("p1")
        try:
            if(check_password(userotp,OTPContainer.objects.get(id=otp).otp)):
                user = NewUser.objects.get(email=email)
                user.password = make_password(password)
                user.save()
                OTPContainer.objects.get(id=otp).delete()
                return render(request,"App/passwordchanged.html")
            else:
                messages.error(request,"You have entered the wrong otp")
        except:
            messages.error(request,"Bad request")
    return render(request,"App/validation.html")
    


@login_required(login_url="App:loginpage")
def logoutuser(request):
    pass
    logout(request)
    return redirect("App:loginpage")


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
def deletePost(request,post_id):
    try:
        post = Post.objects.get(id=post_id)
        # post.delete()
        #the postimage class images are not deleting the while deleting the object of the post so the temporary solution is given here.
        o = PostImage.objects.filter(msg=post_id)
        for i in o:
            i.delete()
        post.delete()
    except:
        pass
        return HttpResponse("error occured")
    return redirect("App:dashboard")

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
        return redirect("App:myaccount")
    context={
        "user":user,
    }
    return render(request,"App/myAccount.html")

@login_required(login_url="App:loginpage")
def deleteavatar(request):
    pass
    user = request.user
    user.avatar = None
    user.save()
    return redirect("App:myaccount") 

