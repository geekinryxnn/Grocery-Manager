from sqlalchemy import Column, Integer, String
from .base import Base

class GroceryList(Base):
    __tablename__ = 'grocery_lists'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    def __repr__(self):
        return f"GroceryList(id={self.id}, name='{self.name}')"