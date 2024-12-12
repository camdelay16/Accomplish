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
    lists = List.objects.all()
    selected_list_id = lists[0].id
    subtask_form = SubtaskForm()
    context = {
        'task': task, 
        'subtask_form': subtask_form, 
        'lists': lists, 
        'selected_list_id': selected_list_id
    }
    return render(request, 'tasks/detail.html', context)

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
    fields = ['list_name', 'description']

class ListIndex(ListView):
    model = List

class ListDetail(DetailView):
    model = List

class ListUpdate(UpdateView):
    model = List
    fields = '__all__'
    success_url='/lists/'

class ListDelete(DeleteView):
    model = List
    success_url = '/lists/'

def associate_list(request, task_id):
    if request.method == 'POST':
        selected_list_id = request.POST.get('selected_list_id')
        if selected_list_id:
            try:
                list_to_associate = List.objects.get(pk=selected_list_id)
                task = Task.objects.get(pk=task_id)
                task.list_key = list_to_associate
                task.save()
                return redirect('task-detail', task_id=task_id)
            except List.DoesNotExist:
                pass
    return redirect('task-detail', task_id=task_id)

def change_list(request, task_id):
    if request.method == 'POST':
        new_list_id = request.POST.get('new_list')
        if new_list_id:
            try:
                task = Task.objects.get(pk=task_id)
                new_list = List.objects.get(pk=new_list_id)
                task.list_key = new_list
                task.save()
                return redirect('task-detail', task_id=task_id)
            except (List.DoesNotExist, Task.DoesNotExist):
                pass
    return redirect('task-detail', task_id=task_id)

def disassociate_list(request, task_id):
    if request.method == 'POST':
        selected_list_id = request.POST.get('selected_list_id')
        if selected_list_id:
            try:
                task = Task.objects.get(pk=task_id)
                task.list_key = None
                task.save()
                return redirect('task-detail', task_id=task_id)
            except List.DoesNotExist:
                pass
    return redirect('task-detail', task_id=task_id)

def change_completed(request, task_id):
    if request.method == 'POST':
        selected_completed_value = request.POST.get('completed')
        if selected_completed_value:
            try:
                task = Task.objects.get(pk=task_id)
                task.completed = selected_completed_value
                task.save()
                return redirect('task-detail', task_id=task_id)
            except Task.DoesNotExist:
                pass
    return redirect('task-detail', task_id=task_id)