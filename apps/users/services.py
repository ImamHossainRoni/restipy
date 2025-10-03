# Add your service code here
from __future__ import annotations
from typing import Optional

from django.db.models import QuerySet, Model
from rest_framework_simplejwt.tokens import RefreshToken
from core.service import ReadService, WriteService
from .dao import UserDAO
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User


class UserReadService(ReadService):
    @property
    def dao_cls(self):
        return UserDAO

    def get_by_username(self, username: str) -> User | None:
        return self.dao.find_one({'username': username})

    def get_all_users(self) -> QuerySet[Model]:
        return self.dao.all()


class UserWriteService(WriteService):
    @property
    def dao_cls(self):
        return UserDAO


class AuthService(ReadService):
    """Handles authentication / token generation"""

    @property
    def dao_cls(self):
        return UserDAO

    @staticmethod
    def get_tokens_for_user(user: User) -> dict:
        refresh = RefreshToken.for_user(user)
        return {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }

    def validate_user(self, email: str, password: str) -> Optional[User]:
        user = self.dao.find_one({'email': email})
        if user and check_password(password, user.password):
            return user
        return None
