from app.crud.base import CRUDBase
from app.models.file_storage import FileStorage
from app.schemas.file_storage import FileStorageCreate, FileStorageUpdate


class CRUDFileStorage(CRUDBase[FileStorage, FileStorageCreate, FileStorageUpdate]):
    pass


file_storage = CRUDFileStorage(FileStorage)
