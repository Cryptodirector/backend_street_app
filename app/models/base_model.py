from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from app.config.db_config import Base
from sqlalchemy import TIMESTAMP
import datetime
from sqlalchemy.sql import func


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    number: Mapped[str] = mapped_column(nullable=False, unique=True)
    telegram_id: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)
    housing_complex_id: Mapped[int] = mapped_column(
        ForeignKey('complex.id'),
        nullable=True
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )


class Copmlex(Base):
    __tablename__ = 'complex'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]


class Jobs(Base):
    __tablename__ = 'jobs'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    user_executor: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
        nullable=True
    )
    user_customer: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
        nullable=True
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=datetime.datetime.now
    )
    jobs_active: Mapped[bool]
    jobs_access: Mapped[bool]


