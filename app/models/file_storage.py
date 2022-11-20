from sqlalchemy import Column, Integer, String
from app.db.base_class import Base


class FileStorage(Base):
    __tablename__ = 't_file_storage'
    __table_args__ = {'schema': 'shop', 'comment': 'Хранилище файлов'}

    id_file = Column(Integer, primary_key=True, index=True, comment="ID")
    name_file = Column(String(100), nullable=False, comment="Имя файла")
    full_path = Column(String(255), nullable=False, comment="Путь к файлу")
