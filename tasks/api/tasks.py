from django.http import HttpRequest
from ninja import Router


router = Router(tags=["tasks"])

@router.get("/")
def index(request: HttpRequest):
    return {"message": "Hello World"}