from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Task, Subtask, List
from .forms import SubtaskForm


# Create your views here.
class Home(LoginView):
    template_name = 'home.html'

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def about(request):
    return render(request, 'about.html')

@login_required
def task_index(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/index.html', {'tasks': tasks})

@login_required
def task_detail(request, task_id):
    task = Task.objects.get(id=task_id)
    lists = List.objects.filter(user=request.user)
    selected_list_id = lists[0].id
    subtask_form = SubtaskForm()
    context = {
        'task': task, 
        'subtask_form': subtask_form, 
        'lists': lists, 
        'selected_list_id': selected_list_id
    }
    return render(request, 'tasks/detail.html', context)

@login_required
def add_subtask(request, task_id):
    form = SubtaskForm(request.POST)
    if form.is_valid():
        new_subtask = form.save(commit=False)
        new_subtask.task_id = task_id
        new_subtask.save()
    return redirect('task-detail', task_id=task_id)

@login_required
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

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['task_name', 'due_date', 'priority', 'note', 'list_key']
    success_url='/tasks/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['task_name', 'due_date', 'priority', 'note', 'list_key']

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = '/tasks/'

class ListCreate(LoginRequiredMixin, CreateView):
    model = List
    fields = ['list_name', 'description']
    success_url='/lists/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class ListIndex(LoginRequiredMixin, ListView):
    model = List
    
    def get_queryset(self):
        user = self.request.user
        return List.objects.filter(user=user)
    
class ListDetail(LoginRequiredMixin, DetailView):
    model = List

class ListUpdate(LoginRequiredMixin, UpdateView):
    model = List
    fields = '__all__'
    success_url='/lists/'

class ListDelete(LoginRequiredMixin, DeleteView):
    model = List
    success_url = '/lists/'

class SubtaskCreate(LoginRequiredMixin, CreateView):
    model = Subtask
    fields = ['subtask_name', 'due_date', 'priority', 'completed']
    
    def get_success_url(self):
        return reverse('task-detail', args=[self.kwargs['task_id']]) 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = Task.objects.get(pk=self.kwargs['task_id'])
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.task_id = self.kwargs['task_id']
        return super().form_valid(form)
    
class SubtaskUpdate(LoginRequiredMixin, UpdateView):
    model = Subtask
    fields = ['subtask_name', 'due_date', 'priority', 'completed']
    
    def get_success_url(self):
        return reverse('task-detail', args=[self.kwargs['task_id']]) 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = Task.objects.get(pk=self.kwargs['task_id'])
        return context

    def form_valid(self, form):
        form.instance.task_id = self.kwargs['task_id']
        return super().form_valid(form)

class SubtaskDelete(LoginRequiredMixin, DeleteView):
    model = Subtask

    def get_success_url(self):
        return reverse('task-detail', args=[self.kwargs['task_id']]) 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = Task.objects.get(pk=self.kwargs['task_id'])
        return context

@login_required
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

@login_required
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

@login_required
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

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)