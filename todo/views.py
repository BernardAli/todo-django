from django.shortcuts import render, redirect, reverse, HttpResponseRedirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import TodoForm
from .models import Todo

# Create your views here.


def get_showing_todos(request, todos):
    if request.GET and request.GET.get('filter'):
        if request.GET.get('filter') == 'completed':
            return todos.filter(is_completed=True)
        if request.GET.get('filter') == 'incomplete':
            return todos.filter(is_completed=False)
    return todos

    return todos


@login_required
def index(request):
    todos = Todo.objects.filter(owner=request.user)
    all_count = todos.count()
    completed_count = todos.filter(is_completed=True).count()
    incomplete_count = todos.filter(is_completed=False).count()
    context = {
        'todos': get_showing_todos(request, todos),
        'completed_count': completed_count,
        'all_count': all_count,
        'incomplete_count': incomplete_count
    }
    return render(request, 'todo/index.html', context)


@login_required
def create_todo(request):
    form = TodoForm()
    context = {
        'form': form
    }

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        is_completed = request.POST.get('is_completed', False)

        todo = Todo()
        todo.title = title
        todo.description = description
        todo.is_completed = True if is_completed == "on" else False
        todo.owner = request.user

        todo.save()
        messages.add_message(request, messages.SUCCESS, 'Todo Created Successfully.')

        return HttpResponseRedirect(reverse('todo_detail', kwargs={'id': todo.pk}))

    return render(request, 'todo/create_todo.html', context)


@login_required
def todo_detail(request, id):
    todo = get_object_or_404(Todo, pk=id)
    context = {
        'todo': todo
    }
    return render(request, 'todo/todo_details.html', context)


@login_required
def todo_delete(request, id):
    todo = get_object_or_404(Todo, id=id)
    context = {
        'todo': todo
    }
    if request.method == 'POST':
        if todo.owner == request.user:
            todo.delete()
            messages.add_message(request, messages.SUCCESS, 'Todo Deleted Successfully.')
            return HttpResponseRedirect(reverse('home'))
        return render(request, 'todo/todo_delete.html', context)


@login_required
def todo_edit(request, id):
    todo = get_object_or_404(Todo, id=id)
    form = TodoForm(instance=todo)
    context = {
        'todo': todo,
        'form': form
    }
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        is_completed = request.POST.get('is_completed', False)

        todo.title = title
        todo.description = description
        todo.is_completed = True if is_completed == "on" else False

        if todo.owner == request.user:
            todo.save()

            messages.add_message(request, messages.SUCCESS, 'Todo Update Success.')
            return HttpResponseRedirect(reverse('todo_detail', kwargs={'id': todo.pk}))
        return render(request, 'todo/todo_edit.html', context)