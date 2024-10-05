from datetime import datetime
from typing import Optional

from django.utils import timezone
from ninja import Schema, Field, FilterSchema
from pydantic import EmailStr, model_validator
from typing_extensions import Self

from tasks.enums import TaskPriority


class CreateTaskSchemaIn(Schema):
    user_email: EmailStr = Field(..., )
    task: str = Field(..., )
    due_by: datetime = Field(..., examples=["2024-10-03T15:49:00"])
    priority: int = Field(..., )
    is_urgent: bool = Field(False, )

    # Validator to check that the due_by is not in the past
    @model_validator(mode="after")
    def validate_date(self) -> Self:
        # Ensure 'due_by' is a valid datetime and is timezone-aware
        if self.due_by and self.due_by.tzinfo is None:
            self.due_by = timezone.make_aware(self.due_by, timezone=timezone.get_current_timezone())

        # Check if the 'due_by' is at least one day in the future
        today: datetime = timezone.make_aware(datetime.today(), timezone=timezone.get_current_timezone())
        if self.due_by is not None and self.due_by.date() <= today.date():
            raise ValueError(f"due_by date {self.due_by.date()} must at least be 1 day in the future")

        return self

    @model_validator(mode="after")
    def validate_is_urgent_and_priority(self) -> Self:
        # Check if is_urgent is True and priority is not High
        if self.is_urgent and self.priority != TaskPriority.HIGH.value:
            raise ValueError("If the task is urgent, the priority must be 'High'.")

        return self

    class Config:
        description = "Request Schema for creating a new task"

class CreateTaskSchemaOut(Schema):
    id: int
    task: str
    user_email: EmailStr
    due_by: datetime
    priority: int
    is_urgent: bool
    created_at: datetime
    updated_at: datetime
    created_by: int

    class Config:
        description = "Response Schema for creating a new task"

class UpdateTaskSchemaIn(Schema):
    id: int = Field(None, )
    user_email: Optional[EmailStr] = Field(None, description="email of the user the task is assigned to")
    task: Optional[str] = Field(None, description="Optional task description")
    due_by: Optional[datetime] = Field(None, description="Optional due date")
    priority: Optional[int] = Field(None, description="Optional task priority")
    is_urgent: Optional[bool] = Field(None, description="Optional urgency flag")

    # Validator to check that the due_by is not in the past
    @model_validator(mode="after")
    def validate_date(self) -> Self:
        # Ensure 'due_by' is a valid datetime and is timezone-aware
        if self.due_by and self.due_by.tzinfo is None:
            self.due_by = timezone.make_aware(self.due_by, timezone=timezone.get_current_timezone())

        # Check if the 'due_by' is at least one day in the future
        today: datetime = timezone.make_aware(datetime.today(), timezone=timezone.get_current_timezone())
        if self.due_by is not None and self.due_by.date() <= today.date():
            raise ValueError(f"due_by date {self.due_by.date()} must at least be 1 day in the future")

        return self

    @model_validator(mode="after")
    def validate_is_urgent_and_priority(self) -> Self:
        # Check if is_urgent is True and priority is not High
        if self.is_urgent and self.priority != TaskPriority.HIGH.value:
            raise ValueError("If the task is urgent, the priority must be 'High'.")

        return self

    class Config:
        description = "Request Schema for updating a task"

class UpdateTaskSchemaOut(Schema):
    id: int
    task: str
    user_email: EmailStr
    due_by: datetime
    priority: int
    is_urgent: bool
    created_at: datetime
    updated_at: datetime
    created_by: int

    class Config:
        description = "Response Schema for updating a task"

class TaskSchemaOut(Schema):
    id: int
    task: str
    user_email: EmailStr
    due_by: datetime
    priority: int
    is_urgent: bool
    created_at: datetime
    updated_at: datetime
    created_by: int

    class Config:
        description = "Response Schema for a task"

class LoginSchema(Schema):
    username: str = Field(..., description="username of the user")
    password: str = Field(..., description="password of the user")

    class Config:
        description = "Login request Schema"

class TokenSchemaOut(Schema):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    class Config:
        description = "Response schema for access and refresh tokens"

class RefreshTokenSchemaIn(Schema):
    refresh_token: str

    class Config:
        description = "Refresh token request Schema"

class TaskFilterSchema(FilterSchema):
    due: bool = None

    class Config:
        description = "Schema to encapsulate GET parameters"