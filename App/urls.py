from django.urls import path
from . import views
app_name="App"
urlpatterns = [
    path("",views.loginpage,name="loginpage"),
    path("forgotpassword/",views.forgotpassword,name="forgotpassword"),
    path("validateotp/<str:email>/<str:otp>",views.validateOTP,name="validateotp"),
    path("signup/",views.signUp,name="signup"),
    path("dashboard/",views.dashboard,name="dashboard"),
    path('like/',views.like,name="like"),
    path("comments/<int:id>",views.comments,name="comments"),
    path("get_comments/<int:id>",views.get_comments,name="getcomments"),
    path("logout",views.logoutuser,name="logout"),
    path("myaccount/",views.myAccount,name='myaccount'),
    path('deleteavatar/',views.deleteavatar,name="deleteavatar"),
]
