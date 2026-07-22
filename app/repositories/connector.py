from typing import TypeVar, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, delete, update
from sqlalchemy.orm import selectinload, InstrumentedAttribute

from app.db.models import Base

ModelType = TypeVar("ModelType", bound=Base)


class Connector:
    def __init__(self, model):
        self.model = model

    async def write_to_db(
        self, data,
        session: AsyncSession,
        commit: bool = True
    ) -> ModelType:
        stmt = insert(self.model).values(data.model_dump()).returning(self.model)
        result = await session.execute(stmt)

        obj = result.scalar()

        await session.flush()

        if commit:
            await session.commit()

        await session.refresh(obj)
        return obj

    async def get_objects(
            self,
            session: AsyncSession,
            offset: int = 0,
            limit: int = 10,
            filters: list | None = None,
    ) -> Sequence[ModelType]:
        stmt = select(self.model)

        if filters:
            stmt = stmt.where(*filters)

        stmt = stmt.offset(offset).limit(limit)
        result = await session.scalars(stmt)
        return result.all()

    async def get_object_by_unic_field(
        self, field_value,
        field: InstrumentedAttribute,
        session: AsyncSession,
        selection_fields: list[InstrumentedAttribute] | None = None
    ) -> ModelType:
        stmt = select(self.model).where(field == field_value)

        if selection_fields is not None:
            for s_field in selection_fields:
                stmt = stmt.options(selectinload(s_field))

        return await session.scalar(stmt)
