from django.urls import path
from . import views
app_name="App"
urlpatterns = [
    path("",views.loginpage,name="loginpage"),
    path("signup/",views.signUp,name="signup"),
    path("dashboard/",views.dashboard,name="dashboard"),
    path('like/',views.like,name="like"),
    path("comments/<int:id>",views.comments,name="comments"),
    path("get_comments/<int:id>",views.get_comments,name="getcomments"),
    path("logout",views.logoutuser,name="logout")
]
