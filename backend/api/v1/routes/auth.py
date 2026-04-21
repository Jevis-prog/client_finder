import hashlib

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status

from api.v1.schemas import CurrentUserOut, RegisterRequest, UserLogin
from config import FASTAPI_COOKIE_SECURE, TOKEN_LENGTH
from services.auth import authenticate_user, create_token_for_user, delete_token, get_user_by_token
from bot.uow.sql import SQLUoW


router = APIRouter()


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


@router.post('/auth/register', status_code=201)
async def register(payload: RegisterRequest) -> None:
    password_hash = _hash_password(payload.password)
    async with SQLUoW() as uow:
        existing = await uow.admin_user_repo.get(username=payload.username)
        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Пользователь уже существует',
            )
        await uow.admin_user_repo.get_or_create(payload.username, password_hash)


@router.post('/login')
async def login(data: UserLogin, response: Response) -> None:
    user = await authenticate_user(
        username=data.username,
        password_hash=data.password_hash,
    )
    if not user:
        raise HTTPException(status_code=401, detail='Неверные учетные данные')

    token_value = await create_token_for_user(user_id=user.id)
    if len(token_value) != TOKEN_LENGTH:
        raise HTTPException(status_code=401, detail='Неверные учетные данные')

    response.set_cookie(
        key='access_token',
        value=token_value,
        httponly=False,
        secure=FASTAPI_COOKIE_SECURE,
        samesite='lax',
        max_age=3600,
    )


@router.post('/logout')
async def logout(response: Response, access_token: str | None = Cookie(None)) -> None:
    response.delete_cookie(key='access_token')
    if access_token:
        await delete_token(access_token)


async def get_current_user(access_token: str | None = Cookie(None)):
    if not access_token:
        raise HTTPException(status_code=401, detail='Не авторизован')
    user = await get_user_by_token(access_token)
    if user is None:
        raise HTTPException(status_code=401, detail='Не авторизован')
    return user


@router.get('/me', response_model=CurrentUserOut)
async def me(user=Depends(get_current_user)) -> CurrentUserOut:
    return CurrentUserOut(
        id=user.id,
        username=user.username,
    )
