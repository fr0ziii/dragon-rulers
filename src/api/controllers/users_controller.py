from fastapi import APIRouter, HTTPException
from typing import List
from src.api.models.user import User, UserCreate
from src.data.db import supabase
import logging
from uuid import UUID, uuid4
import datetime
import bcrypt

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("", response_model=User)
async def create_user(user_create: UserCreate):
    logger.info(f"POST /users - Creating user: {user_create.username}")
    try:
        # Hash the password
        hashed_password = bcrypt.hashpw(user_create.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user_data = {
            "id": str(uuid4()),
            "username": user_create.username,
            "email": user_create.email,
            "password_hash": hashed_password,  # Use password_hash, not password
            "created_at": str(datetime.datetime.now()),
            "updated_at": str(datetime.datetime.now())
        }
        data, count = supabase.table("users").insert(user_data).execute()
        user_data = data[1][0]

    except Exception as e:
        logger.exception(f"Unexpected error creating user: {e}")
        raise

    if user_data:
        return User(
            id=user_data.get(User.ID),
            username=user_data.get(User.USERNAME),
            email=user_data.get(User.EMAIL),
            created_at=str(User.CREATED_AT),
            updated_at=str(User.UPDATED_AT)
        )
    else:
        raise HTTPException(status_code=500, detail="Failed to create user")

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: UUID):
    logger.info(f"GET /users/{user_id} - Getting user")
    try:
        data, count = supabase.table("users").select("*").eq("id", str(user_id)).execute()
        user_data = data[1][0] if data[1] else None
    except Exception as e:
        logger.exception(f"Unexpected error getting user {user_id}: {e}")
        raise

    if user_data:
        return User(
            id=user_data.get(User.ID),
            username=user_data.get(User.USERNAME),
            email=user_data.get(User.EMAIL),
            created_at=str(user_data.get(User.CREATED_AT)),
            updated_at=str(user_data.get(User.UPDATED_AT))
        )
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: UUID, user_create: UserCreate):
    logger.info(f"PUT /users/{user_id} - Updating user: {user_create.username}")
    try:
        # Hash the password if it's provided
        update_data = {
            "username": user_create.username,
            "email": user_create.email,
        }
        if user_create.password:
            update_data["password_hash"] = bcrypt.hashpw(user_create.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        data, count = supabase.table("users").update(update_data).eq("id", str(user_id)).execute()
        user_data = data[1][0]
    except Exception as e:
        logger.exception(f"Unexpected error updating user {user_id}: {e}")
        raise

    if user_data:
        return User(
            id=user_data.get(User.ID),
            username=user_data.get(User.USERNAME),
            email=user_data.get(User.EMAIL),
            created_at=str(user_data.get(User.CREATED_AT)),
            updated_at=str(user_data.get(User.UPDATED_AT))
        )
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.delete("/{user_id}")
async def delete_user(user_id: UUID):
    logger.info(f"DELETE /users/{user_id} - Deleting user")
    try:
        data, count = supabase.table("users").delete().eq("id", str(user_id)).execute()
    except Exception as e:
        logger.exception(f"Unexpected error deleting user {user_id}: {e}")
        raise
    return {"message": "User deleted"}