from sqlalchemy import Column, Integer, String
from .base import Base

class Item(Base):
    __tablename__ = 'items'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    
    def __repr__(self):
        return f"Item(id={self.id}, name='{self.name}', category='{self.category}')"