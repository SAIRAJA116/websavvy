from django.urls import path
from . import views
app_name="Coordinator"
urlpatterns = [
    path("dashboard/",views.dashboard,name="dashboard")
]