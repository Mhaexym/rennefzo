from typing import List
from fastapi import APIRouter, status
from app.api.v1.schemas.item import Item, ItemCreate, ItemUpdate
from app.core.exceptions import NotFoundException

router = APIRouter()

# In-memory storage for demo purposes
# Replace with database in production
items_db: List[Item] = []
next_id = 1


@router.get("/", response_model=List[Item])
def get_items(skip: int = 0, limit: int = 100):
    """Get all items with pagination"""
    return items_db[skip:skip + limit]


@router.get("/{item_id}", response_model=Item)
def get_item(item_id: int):
    """Get a specific item by ID"""
    item = next((item for item in items_db if item.id == item_id), None)
    if not item:
        raise NotFoundException(f"Item with id {item_id} not found")
    return item


@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate):
    """Create a new item"""
    global next_id
    new_item = Item(
        id=next_id,
        **item.model_dump()
    )
    next_id += 1
    items_db.append(new_item)
    return new_item


@router.put("/{item_id}", response_model=Item)
def update_item(item_id: int, item_update: ItemUpdate):
    """Update an existing item"""
    item_index = next(
        (i for i, item in enumerate(items_db) if item.id == item_id),
        None
    )
    if item_index is None:
        raise NotFoundException(f"Item with id {item_id} not found")
    
    existing_item = items_db[item_index]
    update_data = item_update.model_dump(exclude_unset=True)
    updated_item = existing_item.model_copy(update=update_data)
    items_db[item_index] = updated_item
    return updated_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    """Delete an item"""
    item_index = next(
        (i for i, item in enumerate(items_db) if item.id == item_id),
        None
    )
    if item_index is None:
        raise NotFoundException(f"Item with id {item_id} not found")
    
    items_db.pop(item_index)
    return None

