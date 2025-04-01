import shutil
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import desc
from database import get_db
from modal.order import Order, get_next_id
from schema.order import OrderCreate, OrderUpdate
import os

router = APIRouter()

# Directory to store uploaded documents
UPLOAD_DIR = "static"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ✅ Helper function to add file URL to order
def append_filename(order):
    """ Add file URL to order output """
    file_url = f"http://127.0.0.1:8000/{UPLOAD_DIR}/{order.order_req_doc}" if order.order_req_doc != "No document uploaded" else "No document uploaded"

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
        docfile: Optional[UploadFile] = File(),
        db: Session = Depends(get_db)
):
    # raise HTTPException(status_code=404,detail=f"{docfile.filename}")
    # Handle file upload
    # document=docfile.filename
    if docfile != "":
        next_id = get_next_id(db)
        filename = docfile.filename
        file_extension = '.' + filename.split('.')[-1] if '.' in filename else ''

        new_filename = f"{next_id+1}{file_extension}"

        image_path = os.path.join(UPLOAD_DIR, new_filename)

        # ✔️ Save the file
        with open(image_path, "wb") as f:
            shutil.copyfileobj(docfile.file, f)

    # raise HTTPException(status_code=400,detail=f"{file_extension}")
    # return f"{file_extension}"
    else:
        new_filename="that is not work"
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
    orders = db.query(Order).all()

    result = [append_filename(order) for order in orders]

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
        .filter(Order.customer_id == customer_id, Order.is_deleted == False)
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
@router.put("/{order_id}", status_code=200)
def update_order(
        order_id :int,
        customer_id: int = Form(...),
        order_req_comment: str = Form(...),
        status: str = Form(...),
        docfile: Optional[UploadFile] = File(),
        db: Session = Depends(get_db)):
    """ Update an existing order """
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if customer_id:
        order.customer_id = customer_id
    if order_req_comment:
        order.order_req_comment=order_req_comment
    if status:
        order.status = status
    if docfile:
        file_extension = os.path.splitext(docfile.filename)[1]
        new_filename = f"{order_id}{file_extension}"
        docfile_path = os.path.join(UPLOAD_DIR, new_filename)

        with open(docfile_path, "wb") as f:
            f.write(docfile.file.read())

        order.order_req_doc = new_filename

    db.commit()
    db.refresh(order)

    return append_filename(order)
