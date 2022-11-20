from sqlalchemy import Column, Integer, String, Boolean

from app.db.base_class import Base


class Article(Base):
    __tablename__ = "t_article"
    __table_args__ = {"schema": "shop"}

    id_art = Column(Integer, primary_key=True, index=True, comment="ID товара")
    name = Column(String(60), nullable=False, comment="Наименование товара")
    code = Column(String(60), nullable=False, comment="Код товара")
    price = Column(Integer, nullable=False, comment="Цена товара")
    description = Column(String(), comment="Описание товара")
    is_active = Column(Boolean(), comment="Присутствие товара")
