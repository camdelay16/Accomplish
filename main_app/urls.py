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
    path('tasks/<int:task_id>/add-subtask/', views.add_subtask, name='add-subtask'),
    path('lists/create', views.ListCreate.as_view(), name='list-create'),
    path('lists/<int:pk>/', views.ListDetail.as_view(), name='list-detail'),
    path('lists/', views.ListIndex.as_view(), name='list-index'),
    path('lists/<int:pk>/update/', views.ListUpdate.as_view(), name='list-update'),
    path('lists/<int:pk>/delete/', views.ListDelete.as_view(), name='list-delete'),
    path('tasks/<int:task_id>/associate-list/', views.associate_list, name='associate-list'),
    path('tasks/<int:task_id>/change_list/', views.change_list, name='change-list'),
    path('tasks/<int:task_id>/disassociate-list/', views.disassociate_list, name='disassociate-list'),
    path('tasks/<int:task_id>/change_completed', views.change_completed, name='change-completed'),
]