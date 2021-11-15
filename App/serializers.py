from rest_framework import serializers
from .models import *

class CommentSerializer(serializers.ModelSerializer):
    pass
    class Meta:
        model = Comment
        fields="__all__"
        depth = 3
        