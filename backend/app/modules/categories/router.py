from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database.database import get_db
from app.database import crud, schemas, models
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.CategoryResponse])
async def read_categories(db: AsyncSession = Depends(get_db)):
    return await crud.get_categories(db)

@router.post("/", response_model=schemas.CategoryResponse)
async def create_category(
    category: schemas.CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(deps.require_role([models.UserRole.SUPER_ADMIN, models.UserRole.MANAGER])),
):
    return await crud.create_category(db=db, category=category)

@router.put("/{category_id}", response_model=schemas.CategoryResponse)
async def update_category(
    category_id: int,
    category_update: schemas.CategoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(deps.require_role([models.UserRole.SUPER_ADMIN, models.UserRole.MANAGER])),
):
    db_category = await crud.update_category(db=db, category_id=category_id, category_update=category_update)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(deps.require_role([models.UserRole.SUPER_ADMIN, models.UserRole.MANAGER])),
):
    db_category = await crud.delete_category(db=db, category_id=category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted"}
