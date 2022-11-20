from sqlalchemy import Column, Integer, ForeignKey
from app.db.base_class import Base


class ArticleLinkFileStorage(Base):
    __tablename__ = 't_article_link_file_storage'
    __table_args__ = {'schema': 'shop', 'comment': 'Таблица связи товара и фото'}

    id = Column(Integer, primary_key=True, index=True, comment="ID")
    id_art = Column(Integer, ForeignKey("shop.t_article.id_art"), nullable=False, comment="ID товара")
    id_file = Column(Integer, ForeignKey("shop.t_file_storage.id_file"), nullable=False, comment="ID файла")
    position = Column(Integer, nullable=False, comment="Позиция фотографии")