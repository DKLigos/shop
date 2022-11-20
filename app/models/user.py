from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class User(Base):
    __tablename__ = "t_user"
    __table_args__ = {"schema": "shop"}

    id_user = Column(Integer, primary_key=True, index=True)
    username = Column(String(60), nullable=False)
    password = Column(String(60), nullable=False)
