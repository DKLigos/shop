from typing import TypeVar, Generic, List

from pydantic.generics import GenericModel

T = TypeVar('T')


class PaginationResponse(GenericModel, Generic[T]):
    results: int
    rows: List[T]