from django.db import models
from django.utils.translation import gettext_lazy
from django.utils import timezone
import os
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager

# Create your models here.
class CustomAccountManager(BaseUserManager):
    def create_user(self,email,roll,password,**other_fields):
        if not email:
            raise ValueError(gettext_lazy("You must provide an email"))
        email = self.normalize_email(email)
        user = self.model(email=email,roll = roll,**other_fields)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self,email,roll,password,**other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        return self.create_user(email,roll,password,**other_fields)




def get_avataar_path(instance,avatar):
    pass
    return os.path.join("Avatar/{0}/{1}".format(instance.email,instance.avatar))

class NewUser(AbstractBaseUser,PermissionsMixin):
    username = None
    email = models.EmailField(gettext_lazy("email address"),unique=True)
    roll = models.CharField(max_length=10,unique=True)
    firstName = models.CharField(max_length=200,blank=True)
    lastName = models.CharField(max_length=200,blank = True)
    isCoordinator = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    start_date = models.DateField(default=timezone.now)
    avatar = models.ImageField(upload_to=get_avataar_path, blank=True)


    objects = CustomAccountManager()


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['roll','firstName','lastName']

    def __str__(self):
        return self.email+"("+self.roll+")"

    def get_fullname(self):
        return self.firstName+" "+self.lastName

def get_mainimage_path(instance,image):
    return os.path.join("PostImages/{0}/{1}".format(instance.user.email,instance.image))

class Post(models.Model):
    user = models.ForeignKey(NewUser,on_delete=models.CASCADE,related_name="posts")
    message = models.TextField(blank=True,null=True)
    time = models.DateTimeField(auto_now_add=True)
    url = models.URLField(blank=True,null=True)
    image = models.ImageField(upload_to = get_mainimage_path,blank=True,null=True)
    likes = models.ManyToManyField(NewUser,blank=True,default=None,related_name="like")
    like_counter = models.BigIntegerField(default=0)
    def __str__(self):
        return self.user.email

def get_image_path(instance,image):
    return os.path.join("PostImages/{0}/{1}".format(instance.msg.user.email,instance.image))

class PostImage(models.Model):
    msg = models.ForeignKey(Post,on_delete=models.CASCADE)
    image = models.ImageField(upload_to = get_image_path)

    def __str__(self):
        return self.msg.user.email+" "+str(self.msg.id)

class Comment(models.Model):
    msg = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(NewUser,on_delete=models.CASCADE)
    comment = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-time',]
    
    def __str__(self):
        return self.user.email+" to "+self.msg.user.email
    


