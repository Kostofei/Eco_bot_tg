from enum import IntEnum

__all__ = ["UserRole"]


class UserRole(IntEnum):
    USER: int = 1
    ADMIN: int = 2
    SUPER_ADMIN: int = 3
