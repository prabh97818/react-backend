from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
from .models import UserTask


class AllTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTask
        fields = ('id', 'task_name', 'description', 'due_date', 'start_date')
