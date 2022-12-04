from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Metadata(Base):
    __tablename__ = 'metadata'
    id = Column(String(100), primary_key=True)
    imports = Column(Integer, nullable=False)
    exports = Column(Integer, nullable=False)
    path = Column(String(500), nullable=False)
    size = Column(String(100), nullable=False)
    type = Column(String(15), nullable=False)
    arch = Column(String(5), nullable=False)
