from typing import Any

from sqlalchemy import inspect, MetaData
from sqlalchemy.ext.declarative import as_declarative, declared_attr

meta = MetaData(naming_convention={
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(all_column_names)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(all_column_names)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})


@as_declarative(metadata=meta)
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:  # noqa: B902
        return cls.__name__.lower()

    def _asdict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
