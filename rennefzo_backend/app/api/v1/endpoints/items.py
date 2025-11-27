from typing import List
from datetime import datetime
from fastapi import APIRouter, status, Depends
from sqlmodel import Session, select
from app.api.v1.schemas.item import Item, ItemCreate, ItemUpdate
from app.core.exceptions import NotFoundException
from app.db.session import get_session
from app.db.models import Item as ItemModel

router = APIRouter()


@router.get("/", response_model=List[Item])
def get_items(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    """Get all items with pagination"""
    statement = select(ItemModel).offset(skip).limit(limit)
    items = session.exec(statement).all()
    return items


@router.get("/{item_id}", response_model=Item)
def get_item(item_id: int, session: Session = Depends(get_session)):
    """Get a specific item by ID"""
    item = session.get(ItemModel, item_id)
    if not item:
        raise NotFoundException(f"Item with id {item_id} not found")
    return item


@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate, session: Session = Depends(get_session)):
    """Create a new item"""
    db_item = ItemModel(**item.model_dump())
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


@router.put("/{item_id}", response_model=Item)
def update_item(item_id: int, item_update: ItemUpdate, session: Session = Depends(get_session)):
    """Update an existing item"""
    db_item = session.get(ItemModel, item_id)
    if not db_item:
        raise NotFoundException(f"Item with id {item_id} not found")
    
    update_data = item_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    
    db_item.updated_at = datetime.utcnow()
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, session: Session = Depends(get_session)):
    """Delete an item"""
    db_item = session.get(ItemModel, item_id)
    if not db_item:
        raise NotFoundException(f"Item with id {item_id} not found")
    
    session.delete(db_item)
    session.commit()
    return None

