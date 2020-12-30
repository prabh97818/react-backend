from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserTask(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE,  related_name='task')
    task_name = models.CharField(max_length=1000, default="")
    description = models.CharField(max_length=1000, blank=True, default="")
    due_date = models.DateField(auto_now=False, auto_now_add=False)
    start_date = models.DateField(auto_now=False, auto_now_add=False)