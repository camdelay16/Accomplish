from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Task, Subtask, List
from .forms import SubtaskForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def task_index(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/index.html', {'tasks': tasks})

def task_detail(request, task_id):
    task = Task.objects.get(id=task_id)
    subtask_form = SubtaskForm()
    return render(request, 'tasks/detail.html', {'task': task, 'subtask_form': subtask_form})

def add_subtask(request, task_id):
    form = SubtaskForm(request.POST)
    if form.is_valid():
        new_subtask = form.save(commit=False)
        new_subtask.task_id = task_id
        new_subtask.save()
    return redirect('task-detail', task_id=task_id)

def update_subtask(request, task_id, subtask_id):
    subtask = Subtask.objects.get(pk=subtask_id)
    if request.method == 'POST':
        form = SubtaskForm(request.POST, instance=subtask)
        if form.is_valid():
            form.save()
            return redirect('task-detail', task_id=task_id)
    else:
        form = SubtaskForm(instance=subtask)
    context = {'form': form}
    return render(request, 'task_detail.html', context)

class TaskCreate(CreateView):
    model = Task
    fields = '__all__'
    success_url='/tasks/'

class TaskUpdate(UpdateView):
    model = Task
    fields = '__all__'

class TaskDelete(DeleteView):
    model = Task
    success_url = '/tasks/'

class ListCreate(CreateView):
    model = List
    fields = '__all__'

class ListIndex(ListView):
    model = List

class ListDetail(DetailView):
    model = List