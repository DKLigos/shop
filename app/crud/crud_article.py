from app.crud.base import CRUDBase
from app.models import Article
from app.schemas.article import ArticleCreate, ArticleUpdate


class CRUDArticle(CRUDBase[Article, ArticleCreate, ArticleUpdate]):
    pass


article = CRUDArticle(Article)
