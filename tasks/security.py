from django.contrib.auth.models import User
from django.http import HttpRequest
from jwt import InvalidTokenError
from ninja.security import HttpBearer

from tasks.utils import decode_access_token


class JWTAuth(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str):
        try:
            payload = decode_access_token(token)
            username = payload.get("sub")

            if not username:
                return None

            # Get the user from the database in a real world app user instance will be created with claims from token
            #because a JWT is a self-signed token
            try:
                user = User.objects.filter(username=username).first()
                return user
            except User.DoesNotExist:
                return None
        except (InvalidTokenError, ValueError) :
            return None