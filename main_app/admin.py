from django.contrib import admin
from .models import Task, Subtask, List
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Task)
admin.site.register(Subtask)
admin.site.register(List)
