from django.db import models
from django.urls import reverse

# Create your models here.
class Task(models.Model):
    task_name = models.CharField(max_length=100)
    due_date = models.DateField('Due Date')

    class PriorityChoices(models.TextChoices):
        LOW = 'Low', 'Low'
        MEDIUM = 'Medium', 'Medium'
        HIGH = 'High', 'High'

    priority = models.CharField(max_length=10, choices=PriorityChoices.choices, default=PriorityChoices.LOW)
    note = models.TextField(max_length=200)

    class CompletedChoices(models.TextChoices):
        NOT_COMPLETED = 'Not Completed', 'Not Completed'
        COMPLETED = 'Completed', 'Completed'

    completed = models.CharField(max_length=15, choices=CompletedChoices.choices, default=CompletedChoices.NOT_COMPLETED)

    def __str__(self):
        return f"{self.task_name} on {self.due_date}"
    
    def get_absolute_url(self):
        return reverse("task-detail", kwargs={"task_id": self.id})

class Subtask(models.Model):
    subtask_name = models.CharField('Name', max_length=100)
    due_date = models.DateField('Due Date')
    
    class PriorityChoices(models.TextChoices):
        LOW = 'Low', 'Low'
        MEDIUM = 'Medium', 'Medium'
        HIGH = 'High', 'High'

    priority = models.CharField(max_length=10, choices=PriorityChoices.choices, default=PriorityChoices.LOW)

    note = models.TextField(max_length=150)

    class CompletedChoices(models.TextChoices):
        NOT_COMPLETED = 'Not Completed', 'Not Completed'
        COMPLETED = 'Completed', 'Completed'

    completed = models.CharField(max_length=15, choices=CompletedChoices.choices, default=CompletedChoices.NOT_COMPLETED)

    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subtask_name} on {self.due_date}"
    
class List(models.Model):
    list_name = models.CharField('Name', max_length=100)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.list_name
    
    def get_absolute_url(self):
        return reverse("list-detail", kwargs={"list_id": self.id})
