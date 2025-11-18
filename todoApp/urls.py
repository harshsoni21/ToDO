from django.urls import path
from .views import (todo_app_page,todo_list_create_tasks, todo_get_delete_task,todo_update_task
)

urlpatterns = [
    path('Todo/Home/' , todo_app_page , name="Todo App"),
    path('Todo/APIv1/tasks/', todo_list_create_tasks, name="todo_list_create"),
    path('Todo/APIv1/tasks/<int:task_id>/', todo_get_delete_task, name="todo_detail"),
    path('Todo/APIv1/tasks/<int:task_id>/update/', todo_update_task, name="todo_update"),
]
