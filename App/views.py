from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout


# Create your views here.
def loginpage(request):
    if(request.method=="POST"):
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(email=email, password=password)
        if (user is not None):
            login(request,user)
            return redirect("App:dashboard")
    return render(request,"App/loginpage.html")

def dashboard(request):
    return HttpResponse