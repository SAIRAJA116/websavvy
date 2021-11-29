from django.contrib import admin
from .models import *
# Register your models here.
class UserAdminConfig(admin.ModelAdmin):
    ordering=("roll","email")
    list_display = ('email','roll',"isCoordinator")
    search_fields = ('email','roll')

admin.site.register(NewUser,UserAdminConfig)
admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(Comment)
admin.site.register(Event)
admin.site.register(OTPContainer)