from django.urls import path
from . import views
app_name="Coordinator"
urlpatterns = [
    path("dashboard/",views.dashboard,name="dashboard"),
    path("comments/<int:id>",views.comments,name="comments"),
    path("deletepost/<int:post_id>",views.deletePost,name="deletepost"),
    path("myaccount/",views.myAccount,name='myaccount'),
    path('deleteavatar/',views.deleteavatar,name="deleteavatar")
]