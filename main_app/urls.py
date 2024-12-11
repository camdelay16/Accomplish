from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('tasks/', views.task_index, name='task-index'),
    path('tasks/<int:task_id>/', views.task_detail, name='task-detail'),
    path('tasks/create/', views.TaskCreate.as_view(), name='task-create'),
    path('tasks/<int:pk>/update', views.TaskUpdate.as_view(), name='task-update'),
    path('tasks/<int:pk>/delete', views.TaskDelete.as_view(), name='task-delete'),
    path('tasks.<int:task_id>/add-subtask/', views.add_subtask, name='add-subtask'),
    path('lists/create', views.ListCreate.as_view(), name='list-create'),
    path('lists/<int:pk>/', views.ListDetail.as_view(), name='list-detail'),
    path('lists/', views.ListIndex.as_view(), name='list-index'),
]