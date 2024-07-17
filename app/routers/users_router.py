from fastapi import APIRouter, Depends
from app.schemas.user_schemas import (
    RegSchemas,
    LogSchemas,
    LogResponseSchemas,
    UpdateUserSchema
)
from app.service.auth import AuthService
from app.config.db_config import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix='/api',
    tags=['Пользователь']
)


@router.post(
    '/users/registration',
    response_model=RegSchemas,
)
async def registration(
        body: RegSchemas,
        session: AsyncSession = Depends(get_async_session),

) -> RegSchemas:
    return await AuthService.registration_user(
        body,
        session
    )


@router.post(
    '/users/login',
    response_model=LogResponseSchemas
)
async def login(
        body: LogSchemas,
        session: AsyncSession = Depends(get_async_session),
) -> LogResponseSchemas:

    return await AuthService.login_user(
        body,
        session
    )


@router.patch(
    '/users/me/update',
    response_model=UpdateUserSchema
)
async def update(
        body: UpdateUserSchema,
        id: int,
        session: AsyncSession = Depends(get_async_session),

) -> UpdateUserSchema:

    return await AuthService.update(
        body,
        id,
        session
    )


@router.delete(
    '/users/me/delete',
    response_model=None
)
async def delete(
        id: int,
        session: AsyncSession = Depends(get_async_session),

) -> None:

    return await AuthService.delete_user(
        id,
        session
    )

