from django.http import HttpResponse, HttpRequest
from ninja import Router

from tasks.schemas import TokenSchemaOut, LoginSchema, RefreshTokenSchemaIn
from tasks.services import auth_service as services

auth_router = Router()


@auth_router.post("/login", response={200: TokenSchemaOut}, auth=None)
def login(request: HttpRequest, payload: LoginSchema):
    return services.login(request, payload)


@auth_router.post("/refresh-token", response={200: TokenSchemaOut})
def refresh_token(request: HttpRequest, payload: RefreshTokenSchemaIn):
    return services.refresh_token(payload)
