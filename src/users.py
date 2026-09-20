import uuid 
from typing import Optional
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, models
from fastapi_users.authentication import (AuthenticationBackend, BearerTransport, JWTStrategy)
from fastapi_users.db import SQLAlchemyUserDatabase
from src.db import User, user_db

Secret = "aifhjdgigasigidfgifgiosdf"

class User_Manager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = Secret
    verification_token_secret = Secret

    async def on_after_register(self, User, request: Optional[Request] = None):
        pass

    async def on_after_request_verify(self, user: User, token: str, request: Optional[Request] = None):
        pass

async def user_db_manager(user_db: SQLAlchemyUserDatabase = Depends(user_db)):
    yield User_Manager(user_db)

bearer = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy():
    return JWTStrategy(secret=Secret, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer,
    get_strategy=get_jwt_strategy
)

fastapi_users = FastAPIUsers[User, uuid.UUID](user_db_manager, [auth_backend])
current_users = fastapi_users.current_user(active=True)