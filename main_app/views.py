from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django import forms
from .models import Task, Subtask, List
from .forms import SubtaskForm, TaskForm, SignUpForm, UpdateUserForm, ChangePasswordForm


# Create your views here.
class Home(LoginView):
    template_name = 'home.html'

@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)
    lists = List.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'tasks': tasks, 'lists': lists})

def about(request):
    return render(request, 'about.html')

@login_required
def task_index(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/index.html', {'tasks': tasks})

@login_required
def task_priority(request):
    tasks = Task.objects.filter(user=request.user)
    high_priority_tasks = tasks.filter(priority='High')
    medium_priority_tasks = tasks.filter(priority='Medium')
    low_priority_tasks = tasks.filter(priority='Low')

    user_agent = request.META['HTTP_USER_AGENT']
    if 'Mobile' in user_agent:
        slice_size = 1
    else:
        slice_size = 3

    sliced_tasks = []
    for i in range(0, len(tasks), slice_size):
        sliced_tasks.append(tasks[i:i+slice_size])

    sliced_high_priority_tasks = []
    for i in range(0, len(high_priority_tasks), slice_size):
        sliced_high_priority_tasks.append(high_priority_tasks[i:i+slice_size])
    
    sliced_medium_priority_tasks = []
    for i in range(0, len(medium_priority_tasks), slice_size):
        sliced_medium_priority_tasks.append(medium_priority_tasks[i:i+slice_size])

    sliced_low_priority_tasks = []
    for i in range(0, len(low_priority_tasks), slice_size):
        sliced_low_priority_tasks.append(low_priority_tasks[i:i+slice_size])

    context = {
        'tasks': tasks, 
        'sliced_tasks': sliced_tasks,
        'high_priority_tasks': sliced_high_priority_tasks,
        'medium_priority_tasks': sliced_medium_priority_tasks,
        'low_priority_tasks': sliced_low_priority_tasks,
    }
    return render(request, 'tasks/priority.html', context)

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
    fields = ['task_name', 'due_date', 'priority', 'note', 'list_key', 'completed']
    success_url='/tasks/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['task_name', 'due_date', 'priority', 'note', 'list_key', 'completed']

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
    fields = ['list_name', 'description']
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
    form = SignUpForm()
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('dashboard')
        else:
            error_message = 'Invalid sign up - try again'
    else:
        return render(request, 'signup.html', {'form':form})

@login_required
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "User has been updated!")
            return redirect('dashboard')
        return render(request, 'update_user.html', {"user_form": user_form})
    else:
        messages.success(request, "You must be logged in to access page.")
        return redirect('home')

@login_required
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been updated.")
                login(request, current_user)
                return redirect('update-user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return render(request, 'update_password.html', {'form': form})
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form})
    else:
        messages.success(request, "You must be logged in to see this page.")
        return redirect('home')