from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import User, Address
from app.schemas.schemas import UserCreate, UserUpdate, UserResponse
import os
import shutil
from app.core.config import settings

router = APIRouter()

@router.get("/", response_model=List[UserResponse])
async def get_all_users(db: Session = Depends(get_db)):
    """Get all users with their addresses"""
    users = db.query(User).all()
    return users

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a specific user by ID"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        occupation=user.occupation
    )
    db.add(db_user)
    db.flush()

    db_address = Address(
        address_line_one=user.address.address_line_one,
        address_line_two=user.address.address_line_two,
        city=user.address.city,
        country=user.address.country,
        user_id=db_user.id
    )
    db.add(db_address)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(user_id == User.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in user.dict(exclude_unset=True).items():
        if field != "address":
            setattr(db_user, field, value)

    if user.address:
        if db_user.address:
            for field, value in user.address.dict(exclude_unset=True).items():
                setattr(db_user.address, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/{user_id}/profile-picture")
async def upload_profile_picture(user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(user_id == User.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    file_extension = os.path.splitext(file.filename)[1]
    file_name = f"user_{user_id}_profile{file_extension}"
    file_path = os.path.join(settings.UPLOAD_DIR, file_name)

    if db_user.profile_picture and os.path.exists(db_user.profile_picture):
        os.remove(db_user.profile_picture)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db_user.profile_picture = file_path
    db.commit()
    return {"filename": file_name}


@router.delete("/{user_id}/address")
async def delete_address(user_id: int, db: Session = Depends(get_db)):
    db_address = db.query(Address).filter(user_id == Address.user_id).first()
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")

    db.delete(db_address)
    db.commit()
    return {"message": "Address deleted successfully"}


@router.delete("/{user_id}")
async def delete_user_and_address(user_id: int, db: Session = Depends(get_db)):
    # Step 1: Find the user by user_id
    db_user = db.query(User).filter(user_id == User.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Step 2: Delete the associated address if it exists
    db_address = db.query(Address).filter(user_id == Address.user_id).first()
    if db_address:
        db.delete(db_address)

    # Step 3: Delete the profile picture from the server if it exists
    if db_user.profile_picture and os.path.exists(db_user.profile_picture):
        os.remove(db_user.profile_picture)

    # Step 4: Delete the user
    db.delete(db_user)
    db.commit()

    return {"message": "User and associated address deleted successfully"}