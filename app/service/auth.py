from app.models.base_model import Users
from sqlalchemy import insert, select, update, delete
from app.config.db_config import get_async_session
from fastapi import Depends, HTTPException
from app.schemas.user_schemas import (
    RegSchemas,
    LogSchemas,
    LogResponseSchemas,
    UpdateUserSchema
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.security import get_password_hash, verify_password


class AuthService:

    @staticmethod
    async def registration_user(
            body: RegSchemas,
            session: AsyncSession = Depends(
                get_async_session
            )
    ) -> RegSchemas:
        body.password = await get_password_hash(
            body.password
        )
        await session.execute(
            insert(Users).values(
                body.dict()
            )
        )
        await session.commit()
        return body

    @staticmethod
    async def login_user(
            body: LogSchemas,
            session: AsyncSession = Depends(
                get_async_session
            )
    ) -> LogResponseSchemas:
        user = await session.execute(
            select(Users).where(
                Users.number == body.number
            )
        )

        for item in user.scalars().all():
            if item is not None:
                password = await verify_password(
                    body.password,
                    item.password
                )
                if password is True:
                    return LogResponseSchemas(id=item.id)
            else:
                raise HTTPException(
                    status_code=404,
                    detail='User not found'
                )

    @staticmethod
    async def update(
            body: UpdateUserSchema,
            id: int,
            session: AsyncSession = Depends(
                get_async_session
            )
    ) -> UpdateUserSchema:
        user = await session.execute(
            select(Users).where(Users.id == id)
        )

        for item in user.scalars().all():
            if item.number is None:
                raise HTTPException(
                    status_code=404, detail="User not found"
                )

            # Обновление полей пользователя
            update_data = body.dict(exclude_unset=True)

            if 'password' in update_data:
                update_data['password'] = await get_password_hash(
                    update_data['password']
                )

            stmt = (
                update(Users).
                where(Users.id == id).
                values(**update_data)
            )

            await session.execute(stmt)
            await session.commit()
            return body

    @staticmethod
    async def delete_user(
            id: int,
            session: AsyncSession = Depends(
                get_async_session
            )
    ) -> None:

        user = await session.execute(
            delete(Users).where(Users.id == id)
        )
        if user is not None:
            await session.commit()
        else:
            raise HTTPException(
                status_code=404,
                detail='User not found'
            )


