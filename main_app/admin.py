from django.contrib import admin
from .models import Task, Subtask, List

# Register your models here.
admin.site.register(Task)
admin.site.register(Subtask)
admin.site.register(List)