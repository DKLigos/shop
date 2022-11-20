from typing import List, Optional
from pydantic import BaseModel


class FileStorageBase(BaseModel):
    name_file: str
    full_path: str


class FileStorageCreate(FileStorageBase):
    pass


class FileStorageUpdate(FileStorageBase):
    pass


class FileStorageRemove(BaseModel):
    id_file: List[int]


class FileStorageDBBase(FileStorageBase):
    id_file: int

    class Config:
        orm_mode = True
