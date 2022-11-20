from pydantic import BaseModel


class ArticleLinkFileStorageBase(BaseModel):
    id_art: int
    id_file: int
    position: int


class ArticleLinkFileStorageCreate(ArticleLinkFileStorageBase):
    pass


class ArticleLinkFileStorageUpdate(ArticleLinkFileStorageBase):
    id: int
    pass