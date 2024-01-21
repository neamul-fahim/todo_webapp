from rest_framework import serializers
from .models import Todo


class TodoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = "__all__"
        read_only_fields = ("user",)
