from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.http import  HttpResponse
from ninja import Router, Query
from ninja.pagination import paginate

from tasks.services import task_service as services
from tasks.schemas import CreateTaskSchemaOut, CreateTaskSchemaIn, UpdateTaskSchemaIn, UpdateTaskSchemaOut, \
    TaskSchemaOut, TaskFilterSchema
from tasks.security import JWTAuth

tasks_router = Router(tags=["tasks"])

@tasks_router.post("/", response= {201: CreateTaskSchemaOut}, auth=JWTAuth())
def create_task(request, payload: CreateTaskSchemaIn):
    current_user = request.auth
    return services.create_task(current_user, payload)


@tasks_router.put("/{int:task_id}" , response= {200: UpdateTaskSchemaOut}, auth=JWTAuth())
def update_task(request, task_id: int, payload: UpdateTaskSchemaIn):
    payload.id = task_id
    return services.update_task(payload)


@tasks_router.delete("/{int:task_id}", auth=JWTAuth())
def delete_task(request, task_id: int):
    services.delete_task(task_id=task_id)
    return HttpResponse(status=HTTPStatus.NO_CONTENT)


@tasks_router.get("/{int:task_id}", response=TaskSchemaOut, auth=JWTAuth())
def get_task(request, task_id: int):
    return services.get_task(task_id)


@tasks_router.get("/", response=list[TaskSchemaOut], auth=JWTAuth())
@paginate
def list_tasks(request, filters: TaskFilterSchema = Query()):
    return services.list_tasks(filters)