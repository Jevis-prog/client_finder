from fastapi import APIRouter, Cookie, Depends, HTTPException, Response

from api.v1.schemas import CurrentUserOut, UserLogin
from config import FASTAPI_COOKIE_SECURE, SESSION_COOKIE_NAME, TOKEN_EXPIRE_MINUTES, TOKEN_LENGTH
from services.auth import authenticate_user, create_token_for_user, delete_token, get_user_by_token


router = APIRouter()


@router.post('/login')
async def login(data: UserLogin, response: Response) -> None:
    user = await authenticate_user(
        username=data.username,
        password=data.password,
    )
    if not user:
        raise HTTPException(status_code=401, detail='Неверные учетные данные')

    token_value = await create_token_for_user(user_id=user.id)
    if len(token_value) != TOKEN_LENGTH:
        raise HTTPException(status_code=401, detail='Неверные учетные данные')

    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token_value,
        httponly=True,
        secure=FASTAPI_COOKIE_SECURE,
        samesite='strict',
        max_age=TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post('/logout')
async def logout(response: Response, access_token: str | None = Cookie(None, alias=SESSION_COOKIE_NAME)) -> None:
    response.delete_cookie(
        key=SESSION_COOKIE_NAME,
        secure=FASTAPI_COOKIE_SECURE,
        httponly=True,
        samesite='strict',
    )
    if access_token:
        await delete_token(access_token)


async def get_current_user(access_token: str | None = Cookie(None, alias=SESSION_COOKIE_NAME)):
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
