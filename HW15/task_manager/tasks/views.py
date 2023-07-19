from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Task, Category, Tag
from django.core.paginator import Paginator


def home(request):
    tasks = Task.objects.all()
    paginator = Paginator(tasks, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "home.html", {"page_obj": page_obj})


def search(request):
    query = request.GET.get("query", None)
    if query is not None:
        tasks = Task.objects.filter(title__icontains=query) | Task.objects.filter(
            tags__name__icontains=query
        )
        return render(request, "search.html", {"tasks": tasks})
    else:
        return render(request, "search.html", {})


def task(request, task_id):
    task = Task.objects.get(id=task_id)
    return render(request, "task.html", {"task": task})


def task_page(request):
    tasks_todo = Task.objects.filter(status="to-do")
    tasks_in_progress = Task.objects.filter(status="in-progress")
    tasks_done = Task.objects.filter(status="done")

    context = {
        "tasks_todo": tasks_todo,
        "tasks_in_progress": tasks_in_progress,
        "tasks_done": tasks_done,
    }
    return render(request, "task_page.html", context)


def all_categories(request):
    categories = Category.objects.all()
    return render(request, "categories.html", {"categories": categories})


def autocomplete_data(request):
    task_titles = Task.objects.values_list("title", flat=True)
    tag_names = Tag.objects.values_list("name", flat=True)

    autocomplete_data = list(task_titles) + list(tag_names)

    return JsonResponse(autocomplete_data, safe=False)
