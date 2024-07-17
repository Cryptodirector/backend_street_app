from typing import Any, Sequence

from fastapi import APIRouter, Depends
from fastapi_redis_cache import cache
from sqlalchemy import Row, RowMapping

from app.schemas.jobs_schemas import (
    JobsSchemas
)
from app.config.db_config import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.service.jobs import JobsService

router = APIRouter(
    prefix='/api',
    tags=['Работа']
)


# Создать заявку

@router.post(
    '/jobs',
    response_model=JobsSchemas
)
async def jobs_add(
        body: JobsSchemas,
        session: AsyncSession = Depends(
            get_async_session
        )
) -> JobsSchemas:
    return await JobsService.add(
        body,
        session
    )


# Посмотреть заявки


@router.get(
    '/jobs',
    response_model=None
)
@cache(expire=20)
async def jobs_get(
        session: AsyncSession = Depends(
            get_async_session
        )
) -> Sequence[Row[Any] | RowMapping | Any]:
    return await JobsService.read(session)


# Получить одну заявку

@router.get(
    '/jobs/{id}',
    response_model=None
)
async def get_current_job(
        id: int,
        session: AsyncSession = Depends(
            get_async_session
        )
) -> Sequence[Row[Any] | RowMapping | Any]:
    return await JobsService.read_current_job(
        id,
        session
    )


# Получить все мои выполненные заказы


@router.get(
    '/jobs/my/{my_id}/access',
    response_model=None
)
async def get_access_job(
        my_id: int,
        session: AsyncSession = Depends(
            get_async_session
        )
) -> Sequence[Row[Any] | RowMapping | Any]:
    return await JobsService.my_access_jobs(
        my_id,
        session
    )


# Получить все мои активные заказы


@router.get(
    '/jobs/my/{my_id}/active',
    response_model=None
)
async def get_access_jobs(
        my_id: int,
        session: AsyncSession = Depends(
            get_async_session
        )
) -> Sequence[Row[Any] | RowMapping | Any]:
    return await JobsService.my_active_jobs(
        my_id,
        session
    )


# Удалить мой заказ


@router.delete(
    '/jobs/my/{my_id}/{id}/delete',
    response_model=None
)
async def delete_my_job(
        id: int,
        my_id: int,
        session: AsyncSession = Depends(
            get_async_session
        )
) -> None:
    return await JobsService.delete_jobs(
        id,
        my_id,
        session
    )


# Взять заказ


@router.post(
    '/jobs/{id}/take',
    response_model=None
)
async def take(
        id: int,
        my_id: int,
        session: AsyncSession = Depends(
            get_async_session
        )
) -> str:
    return await JobsService.take_app(
        id,
        my_id,
        session
    )


@router.post(
    '/jobs/{id}/access',
    response_model=None
)
async def access_app(
        id: int,
        my_id: int,
        session: AsyncSession = Depends(
            get_async_session
        )
) -> None:
    return await JobsService.access_job(
        id,
        my_id,
        session
    )