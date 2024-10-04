from enum import Enum


class TaskPriority(int, Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3