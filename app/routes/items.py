from fastapi import APIRouter, HTTPException
from typing import List
from app.models.item import ItemCreate, ItemUpdate, ItemResponse
from app.repository.item_repository import ItemRepository

router = APIRouter()
repo = ItemRepository()


@router.post("/", response_model=ItemResponse, status_code=201)
def create_item(item: ItemCreate):
    return repo.create(item)


@router.get("/", response_model=List[ItemResponse])
def get_all_items():
    return repo.find_all()


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int):
    item = repo.find_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} not found")
    return item


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: ItemUpdate):
    updated = repo.update(item_id, item)
    if updated is None:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} not found")
    return updated


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int):
    deleted = repo.delete(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} not found")
    return None
