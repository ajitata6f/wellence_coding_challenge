from datetime import datetime

from django.shortcuts import get_object_or_404
from django.utils import timezone

from django.contrib.auth.models import User

from tasks.models import Task
from tasks.schemas import CreateTaskSchemaIn, UpdateTaskSchemaIn, TaskFilterSchema, DashboardSchemaOut


def create_task(current_user: User, payload: CreateTaskSchemaIn) -> Task:
    assignee = get_object_or_404(User, username=payload.user_email)

    task = Task(**payload.dict())
    task.created_by = current_user.id
    task.assignee = assignee #User.objects.get(id=1)
    task.created_at = timezone.now()
    task.save()

    return task


def update_task(payload: UpdateTaskSchemaIn) -> Task:
    task = get_object_or_404(Task, id=payload.id)

    get_object_or_404(User, username=payload.user_email)

    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(task, attr, value)
    task.save()

    return task


def get_task(task_id) -> Task:
    task = get_object_or_404(Task, id=task_id)
    return task


def delete_task(task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()


def list_tasks(filters: TaskFilterSchema) -> list[Task]:
    tasks_query = Task.objects.all()


    if filters.due:
        tasks_query = tasks_query.filter(due_by__lte=timezone.make_aware(datetime.now(), timezone=timezone.get_current_timezone()))

    return tasks_query


def task_report() -> DashboardSchemaOut:

    return DashboardSchemaOut()