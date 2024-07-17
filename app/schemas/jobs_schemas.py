from typing import Annotated, Optional

from pydantic import BaseModel, Field


class JobsSchemas(BaseModel):
    title: Annotated[str, Field(min_length=5, max_length=40)]
    description: Annotated[str, Field(min_length=6, max_length=500)]
    user_executor: Optional[int] = None
    user_customer: int
    jobs_access: Optional[bool] = False
    jobs_active: Optional[bool] = False

    class Config:
        from_attributes = True
