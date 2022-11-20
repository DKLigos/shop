from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select, delete, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import BinaryExpression

from app.db.base_class import Base
from app.schemas import PaginationResponse

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, db: AsyncSession, *args: Any, **kwargs: Any) -> Optional[ModelType]:
        result = await db.execute(select(self.model).filter(*args).filter_by(**kwargs))
        return result.scalars().first()

    async def get_multi(
            self,
            db: AsyncSession,
            *args: Any,
            filters: List[BinaryExpression] = None,
            orders: List[BinaryExpression] = None,
            **kwargs
    ) -> List[ModelType]:
        filters = [] if filters is None else filters
        statement = select(self.model).filter(*args).filter(*filters).filter_by(**kwargs)
        if orders:
            statement = statement.order_by(*orders)
        result = await db.execute(statement)
        return result.scalars().all()

    async def get_multi_export(
            self,
            db: AsyncSession,
            *args: Any,
            filters: List[BinaryExpression] = None,
            **kwargs
    ) -> List[ModelType]:
        filters = [] if filters is None else filters
        statement = select(self.model).filter(*args).filter(*filters).filter_by(
            **kwargs)
        result = await db.execute(statement)
        keys = self.model.__table__.columns.keys()
        return keys, result.scalars().fetchmany

    async def get_multi_pagination(
            self,
            db: AsyncSession,
            *args: Any,
            skip: int = 0,
            limit: int = 100,
            filters: List[BinaryExpression] = None,
            orders: List[BinaryExpression] = None,
            **kwargs
    ) -> PaginationResponse[Type[ModelType]]:

        statement = select(self.model, func.count().over().label('results_cnt')).filter(*args).filter(
            *filters).filter_by(**kwargs).offset(skip).limit(limit)
        if orders:
            statement = statement.order_by(*orders)
        result = await db.execute(statement)

        row = result.fetchone()
        if not row:
            return {'results': 0, 'rows': []}
        rows = [row[0]]
        rows.extend(result.scalars().all())
        return {'results': row[1], 'rows': rows}

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def create_from_data(self, db: AsyncSession, *, obj_in_data: dict) -> ModelType:
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db: AsyncSession,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *args: Any, **kwargs: Any):
        await db.execute(delete(self.model).filter(*args).filter_by(**kwargs))

    async def update_multi(self, db: AsyncSession, *args: Any, values: Dict = None, **kwargs: Any):
        await db.execute(update(self.model).values(**values).where(*args).filter_by(**kwargs))
