from sqlalchemy import Column, Integer, Boolean, ForeignKey
from .base import Base

class ListItem(Base):
    __tablename__ = 'list_items'
    
    id = Column(Integer, primary_key=True)
    list_id = Column(Integer, ForeignKey('grocery_lists.id'))
    item_id = Column(Integer, ForeignKey('items.id'))
    purchased = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"ListItem(id={self.id}, purchased={self.purchased})"