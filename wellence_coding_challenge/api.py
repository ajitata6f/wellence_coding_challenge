from ninja import NinjaAPI

from tasks.api.tasks import tasks_router
from tasks.api.auth import auth_router

api = NinjaAPI()
api.add_router("/tasks/", tasks_router)
api.add_router("/auth/", auth_router)