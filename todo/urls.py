from django.urls import path
from .views import index, create_todo, todo_detail, todo_delete, todo_edit

urlpatterns = [
    path('', index, name='home'),
    path('create/', create_todo, name='create_todo'),
    path('todo/<id>/', todo_detail, name='todo_detail'),
    path('todo-delete/<id>/', todo_delete, name='todo_delete'),
    path('todo-edit/<id>/', todo_edit, name='todo_edit'),
]