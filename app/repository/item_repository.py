import threading
from typing import Dict, List, Optional
from app.models.item import ItemCreate, ItemUpdate, ItemResponse


class ItemRepository:
    """In-memory repository for items (like a Java HashMap-based DAO)."""

    def __init__(self):
        self._store: Dict[int, dict] = {}
        self._counter = 0
        self._lock = threading.Lock()

    def create(self, item: ItemCreate) -> ItemResponse:
        with self._lock:
            self._counter += 1
            record = {
                "id": self._counter,
                "name": item.name,
                "description": item.description,
                "price": item.price,
                "quantity": item.quantity,
            }
            self._store[self._counter] = record
            return ItemResponse(**record)

    def find_all(self) -> List[ItemResponse]:
        with self._lock:
            return [ItemResponse(**v) for v in self._store.values()]

    def find_by_id(self, item_id: int) -> Optional[ItemResponse]:
        with self._lock:
            record = self._store.get(item_id)
            return ItemResponse(**record) if record else None

    def update(self, item_id: int, item: ItemUpdate) -> Optional[ItemResponse]:
        with self._lock:
            record = self._store.get(item_id)
            if record is None:
                return None
            update_data = item.model_dump(exclude_unset=True)
            record.update(update_data)
            return ItemResponse(**record)

    def delete(self, item_id: int) -> bool:
        with self._lock:
            return self._store.pop(item_id, None) is not None
