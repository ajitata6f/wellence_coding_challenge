from datetime import timedelta

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from ninja.errors import HttpError

from tasks.schemas import LoginSchema, TokenSchemaOut, RefreshTokenSchemaIn
from tasks.utils import create_access_token, create_refresh_token, decode_access_token


def login(request, payload: LoginSchema) -> TokenSchemaOut:
    user = authenticate(request, username=payload.username, password=payload.password)

    if not user:
        raise HttpError(status_code=404, message="Invalid username or password")

    # Create access and refresh tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    jwt_access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    jwt_refresh_token = create_refresh_token(data={"sub": user.username}, expires_delta=refresh_token_expires)

    return TokenSchemaOut(access_token=jwt_access_token, refresh_token=jwt_refresh_token, token_type="bearer")


def refresh_token(payload: RefreshTokenSchemaIn) -> TokenSchemaOut:
    try:
        # Decode the refresh token
        payload_data = decode_access_token(payload.refresh_token)
        username = payload_data.get("sub")

        # Ensure the user exists
        user = User.objects.filter(username=username).first()
        if not user:
            raise HttpError(status_code=404, message="User not found")

        # Generate new access token and refresh token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        jwt_access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

        refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        jwt_refresh_token = create_refresh_token(data={"sub": user.username}, expires_delta=refresh_token_expires)

        return TokenSchemaOut(access_token=jwt_access_token, refresh_token=jwt_refresh_token, token_type="bearer")
    except ValueError as e:
        raise HttpError(status_code=401, message=f"{str(e)}")
