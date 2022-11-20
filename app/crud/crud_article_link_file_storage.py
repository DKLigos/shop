from app.crud.base import CRUDBase
from app.models import ArticleLinkFileStorage
from app.schemas import ArticleLinkFileStorageCreate, ArticleLinkFileStorageUpdate


class CRUDArticleLinkFileStorage(CRUDBase[ArticleLinkFileStorage, ArticleLinkFileStorageCreate, ArticleLinkFileStorageUpdate]):
    pass


article_link_file_storage = CRUDArticleLinkFileStorage(ArticleLinkFileStorage)
