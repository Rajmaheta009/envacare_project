from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import desc
from database import get_db
from modal.order import Order, get_next_id
from schema.order import OrderCreate, OrderUpdate, OrderOut
import os

router = APIRouter()

# Directory to store uploaded documents
UPLOAD_DIR = "static/upload"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ✅ Helper function to add file URL to order
def append_filename(order):
    """ Add file URL to order output """
    file_url = f"http://127.0.0.1:8000/static/{order.order_req_doc}" if order.order_req_doc != "No document uploaded" else "No document uploaded"

    return {
        "id": order.id,
        "customer_id": order.customer_id,
        "order_req_comment": order.order_req_comment,
        "order_req_doc": file_url,
        "status": order.status,
    }


# ✅ Create a new order with file upload
@router.post("/", response_model=dict)
async def create_order(
        customer_id: int = Form(...),
        order_req_comment: str = Form(...),
        status: str = Form(...),
        docfile: Optional[UploadFile] = File(None),
        db: Session = Depends(get_db)
):
    """ Create a new order with optional file upload """
    image_path = "No document uploaded"

    # Handle file upload
    if docfile:
        next_id = get_next_id(db)
        file_extension = os.path.splitext(docfile.filename)[1]  # Keeps original extension
        new_filename = f"{next_id}{file_extension}"
        image_path = os.path.join(new_filename)

        # Save file
        with open(image_path, "wb") as f:
            f.write(docfile.file.read())

    # Create new order record
    new_order = Order(
        customer_id=customer_id,
        order_req_comment=order_req_comment,
        order_req_doc=new_filename,
        status=status,
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return append_filename(new_order)


# ✅ Get all orders (excluding soft deleted)
@router.get("/")
def get_orders(db: Session = Depends(get_db)):
    """ Retrieve all non-deleted orders with filenames """
    orders = db.query(Order).filter(Order.is_deleted == False).all()

    result = []
    for order in orders:
        result.append(append_filename(order))

    return result


# ✅ Get order by ID (excluding soft deleted)
@router.get("/order_id/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    """ Retrieve a single order by ID """
    order = db.query(Order).filter(Order.id == order_id, Order.is_deleted == False).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found or deleted")

    return append_filename(order)


# ✅ Get latest order by customer ID (excluding soft deleted)
@router.get("/customer_id/{customer_id}")
def get_order_by_customer_id(customer_id: int, db: Session = Depends(get_db)):
    """ Retrieve the latest order by customer ID """
    latest_order = (
        db.query(Order)
        .filter(Order.customer_id == customer_id)
        .order_by(desc(Order.created_at))
        .first()
    )

    if not latest_order:
        raise HTTPException(status_code=404, detail="Order not found or deleted")

    return append_filename(latest_order)


# ✅ Soft delete an order (set is_deleted=True, is_active=False)
@router.delete("/{order_id}", response_model=dict)
def soft_delete_order(order_id: int, db: Session = Depends(get_db)):
    """ Soft delete the order by setting is_deleted=True and is_active=False """
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.is_deleted = True
    order.is_active = False

    db.commit()

    return {"message": "Order soft deleted successfully"}


# ✅ Restore a soft-deleted order
@router.put("/restore/{order_id}", response_model=dict)
def restore_order(order_id: int, db: Session = Depends(get_db)):
    """ Restore a soft-deleted order """
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.is_deleted = False
    order.is_active = True

    db.commit()

    return {"message": "Order restored successfully"}


# ✅ Update an order
@router.put("/{order_id}", response_model=dict)
def update_order(order_id: int, order_data: OrderUpdate, db: Session = Depends(get_db)):
    """ Update an existing order """
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    for key, value in order_data.dict(exclude_unset=True).items():
        setattr(order, key, value)

    db.commit()
    db.refresh(order)

    return append_filename(order)
