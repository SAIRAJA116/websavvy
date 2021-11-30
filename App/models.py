from django.db import models
from django.utils.translation import gettext_lazy
from django.utils import timezone
import os
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from datetime import datetime
import os
from PIL import Image  


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

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        if(self.avatar):
            img = Image.open(self.avatar.path)
            if img.height>150 or img.width>150  :
                pass 
                output_size = (150,150)
                img.thumbnail(output_size)
                img.save(self.avatar.path)

def get_mainimage_path(instance,image):
    time = str(instance.time.year)+str(instance.time.month)+str(instance.time.day)+str(instance.time.hour) + str(instance.time.minute) + str(instance.time.second)
    return os.path.join("PostImages/{0}/{1}/{2}".format(instance.user.email,time,instance.image))

class Post(models.Model):
    user = models.ForeignKey(NewUser,on_delete=models.CASCADE,related_name="posts")
    message = models.TextField(blank=True,null=True)
    time = models.DateTimeField(auto_now_add=True)
    url = models.URLField(blank=True,null= True)
    likes = models.ManyToManyField(NewUser,blank=True,default=None,related_name="like")
    like_counter = models.BigIntegerField(default=0)
    is_event = models.BooleanField(default=False)
    image = models.ImageField(upload_to = get_mainimage_path,blank=True,null=True)

    class Meta:
        ordering = ["-time"]


    def __str__(self):
        return self.user.email

    def save(self,*args,**kwargs):
        pass
        super().save(*args,**kwargs)
        if(self.image):
            img = Image.open(self.image.path)
            if(img.height>300 or img.width>300):
                output_size = (300,300)
                img.thumbnail(output_size)
                img.save(self.image.path)

    def delete(self, using=None, keep_parents=False):
        self.image.storage.delete(self.image.name)
        super().delete()

def get_image_path(instance,image):
    time = str(instance.msg.time.year)+str(instance.msg.time.month)+str(instance.msg.time.day)+str(instance.msg.time.hour) + str(instance.msg.time.minute) + str(instance.msg.time.second)
    return os.path.join("PostImages/{0}/{1}/{2}".format(instance.msg.user.email,time,instance.image))

class PostImage(models.Model):
    msg = models.ForeignKey(Post,on_delete=models.CASCADE)
    image = models.ImageField(upload_to = get_image_path)

    def __str__(self):
        return self.msg.user.email+" "+str(self.msg.id)

    def save(self,*args,**kwargs):
        pass
        super().save(*args,**kwargs)
        if(self.image):
            img = Image.open(self.image.path)
            if(img.height>300 or img.width>300):
                output_size = (300,300)
                img.thumbnail(output_size)
                img.save(self.image.path)

    def delete(self,using=None,keep_parents=False):
        self.image.storage.delete(self.image.name)
        super().delete()



class Comment(models.Model):
    msg = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(NewUser,on_delete=models.CASCADE)
    comment = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-time',]
    
    def __str__(self):
        return self.user.email+" to "+self.msg.user.email

def get_eventlogo_path(instance,icon):
    return os.path.join("Eventicon/{0}/{1}".format(instance.title,instance.icon))

class Event(models.Model):
    title = models.CharField(max_length=300)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="events")
    icon = models.ImageField(upload_to = get_eventlogo_path)
    
    def __str__(self):
        return self.title

class OTPContainer(models.Model):
    otp = models.CharField(max_length=1000)
    