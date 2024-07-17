from app.models.base_model import Jobs, Users
from app.schemas.jobs_schemas import JobsSchemas
from sqlalchemy import (
    insert,
    select,
    delete,
    and_,
    Row,
    RowMapping,
    join, update
)
from app.config.db_config import get_async_session
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Sequence


class JobsService:

    @staticmethod
    async def add(
            body: JobsSchemas,
            session: AsyncSession = Depends(
                get_async_session
            )
    ) -> JobsSchemas:

        await session.execute(
            insert(Jobs).values(body.dict())
        )
        await session.commit()
        return body

    @staticmethod
    async def read(
            session: AsyncSession = Depends(
                get_async_session
            )
    ) -> Sequence[Row[Any] | RowMapping | Any]:
        result = await session.execute(
            select(
                Jobs.title,
                Jobs.description,
                Users.name
            ).select_from(
                join(
                    Jobs,
                    Users,
                    Users.id == Jobs.user_customer
                )
            )
        )
        return result.mappings().all()

    @staticmethod
    async def read_current_job(
            id: int,
            session: AsyncSession = Depends(
                get_async_session
            )
    ) -> Sequence[Row[Any] | RowMapping | Any]:
        result = await session.execute(
            select(
                Jobs.title,
                Jobs.description,
                Users.name
            ).select_from(
                join(
                    Jobs,
                    Users,
                    Users.id == Jobs.user_customer
                )
            ).where(Jobs.id == id)
        )
        if result:
            return result.mappings().first()
        else:
            raise HTTPException(
                status_code=404,
                detail='Jobs not found'
            )

    @staticmethod
    async def my_access_jobs(
            my_id: int,
            session: AsyncSession = Depends(
                get_async_session
            )
    ) -> Sequence[Row[Any] | RowMapping | Any]:
        result = await session.execute(
            select(
                Jobs.title,
                Jobs.description,
                Users.name
            ).select_from(
                join(
                    Jobs,
                    Users,
                    Users.id == Jobs.user_customer
                )
            ).where(
                and_(
                    Jobs.jobs_access == True,
                    Jobs.user_executor == my_id
                )
            )
        )
        if result:
            return result.mappings().first()
        else:
            raise HTTPException(
                status_code=404,
                detail='Jobs not found'
            )

    @staticmethod
    async def my_active_jobs(
            my_id: int,
            session: AsyncSession = Depends(
                get_async_session
            )
    ) -> Sequence[Row[Any] | RowMapping | Any]:
        result = await session.execute(
            select(
                Jobs.title,
                Jobs.description,
                Users.name
            ).select_from(
                join(
                    Jobs,
                    Users,
                    Users.id == Jobs.user_customer
                )
            ).where(
                and_(
                    Jobs.jobs_active == True,
                    Jobs.user_executor == my_id
                )
            )
        )

        return result.mappings().all()

    @staticmethod
    async def delete_jobs(
            id: int,
            my_id: int,
            session: AsyncSession = Depends(
                get_async_session
            )
    ) -> None:
        result = await session.execute(
            delete(Jobs).where(
                and_(
                    Jobs.user_customer == my_id,
                    Jobs.id == id
                )
            )
        )

        if result:
            await session.commit()
        else:
            raise HTTPException(
                status_code=404,
                detail='Jobs not found'
            )

    @staticmethod
    async def take_app(
            id: int,
            my_id: int,
            session: AsyncSession = Depends(
                get_async_session
            )
    ) -> str:

        query = await session.execute(
            select(Jobs.user_executor).where(Jobs.id == id)
        )

        if query.scalar() is None:

            await session.execute(
                update(Jobs).values(
                    user_executor=my_id,
                    jobs_active=True
                ).where(Jobs.id == id)
            )
            await session.commit()

            result = await session.execute(
                select(Users.telegram_id).join(
                    Jobs, Jobs.user_executor == my_id
                ).where(Jobs.id == id)
            )
            if result:
                return result.scalar()
            else:
                raise HTTPException(
                    status_code=404,
                    detail='Jobs not found'
                )

    @staticmethod
    async def access_job(
            id: int,
            my_id: int,
            session: AsyncSession = Depends(
                get_async_session
            )
    ) -> None:
        result = await session.execute(
            update(Jobs).values(jobs_access=True).where(
                and_(
                    Jobs.user_customer == my_id,
                    Jobs.id == id
                )
            )
        )

        if result:
            await session.commit()
        else:
            raise HTTPException(
                status_code=404,
                detail='Jobs not found'
            )