from typing import List, Optional
from pydantic import BaseModel, condecimal


class ArticleDB(BaseModel):
    id_art: int
    name: str
    code: str
    price: condecimal(max_digits=18, decimal_places=2)
    description: str
    is_active: Optional[bool]


class ArticleCreate(BaseModel):
    name: str = None
    code: str = None
    price: condecimal(max_digits=18, decimal_places=2) = None
    description: str = None
    is_active: Optional[bool] = None


class ArticleUpdate(BaseModel):
    id_art: int
    name: Optional[str]
    code: Optional[str]
    price: Optional[condecimal(max_digits=18, decimal_places=2)]
    description: Optional[str]
    is_active: Optional[bool]


class ArticlesRemove(BaseModel):
    id_articles: List[int]
