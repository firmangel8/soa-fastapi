from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_items():
    return [{"id": 1, "item": "Book"}, {"id": 2, "item": "Pen"}]

@router.get("/{item_id}")
def get_item(item_id: int):
    return {"id": item_id, "item": f"Item {item_id}"}
