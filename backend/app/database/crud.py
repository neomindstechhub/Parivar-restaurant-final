from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.database import models, schemas

async def get_categories(db: AsyncSession):
    result = await db.execute(select(models.Category).options(selectinload(models.Category.menu_items)))
    return result.scalars().all()

async def create_category(db: AsyncSession, category: schemas.CategoryCreate):
    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

async def get_category_by_name(db: AsyncSession, name: str):
    result = await db.execute(select(models.Category).filter(models.Category.name == name))
    return result.scalars().first()

async def update_category(db: AsyncSession, category_id: int, category_update: schemas.CategoryUpdate):
    result = await db.execute(select(models.Category).filter(models.Category.id == category_id))
    db_category = result.scalars().first()
    if db_category:
        update_data = category_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_category, key, value)
        await db.commit()
        await db.refresh(db_category)
    return db_category

async def delete_category(db: AsyncSession, category_id: int):
    result = await db.execute(select(models.Category).filter(models.Category.id == category_id))
    db_category = result.scalars().first()
    if db_category:
        await db.delete(db_category)
        await db.commit()
    return db_category

async def get_menu_items_by_category(db: AsyncSession, category_name: str):
    result = await db.execute(
        select(models.MenuItem)
        .join(models.Category)
        .filter(models.Category.name == category_name)
        .order_by(models.MenuItem.id)
    )
    return result.scalars().all()

async def get_menu_items(db: AsyncSession):
    result = await db.execute(select(models.MenuItem).order_by(models.MenuItem.id))
    return result.scalars().all()

async def create_menu_item(db: AsyncSession, menu_item: schemas.MenuItemCreate):
    db_menu_item = models.MenuItem(**menu_item.model_dump())
    db.add(db_menu_item)
    await db.commit()
    await db.refresh(db_menu_item)
    return db_menu_item

async def update_menu_item(db: AsyncSession, item_id: int, menu_item_update: schemas.MenuItemUpdate):
    result = await db.execute(select(models.MenuItem).filter(models.MenuItem.id == item_id))
    db_item = result.scalars().first()
    if db_item:
        update_data = menu_item_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)
        await db.commit()
        await db.refresh(db_item)
    return db_item

async def delete_menu_item(db: AsyncSession, item_id: int):
    result = await db.execute(select(models.MenuItem).filter(models.MenuItem.id == item_id))
    db_item = result.scalars().first()
    if db_item:
        await db.delete(db_item)
        await db.commit()
    return db_item

async def get_users(db: AsyncSession):
    result = await db.execute(select(models.User))
    return result.scalars().all()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    from app.core import security
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        role=user.role,
        is_active=user.is_active,
        password_hash=hashed_password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_user(db: AsyncSession, user_id: int, user_update: schemas.UserUpdate):
    from app.core import security
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    db_user = result.scalars().first()
    if db_user:
        update_data = user_update.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["password_hash"] = security.get_password_hash(update_data.pop("password"))
        for key, value in update_data.items():
            setattr(db_user, key, value)
        await db.commit()
        await db.refresh(db_user)
    return db_user

async def delete_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    db_user = result.scalars().first()
    if db_user:
        await db.delete(db_user)
        await db.commit()
    return db_user
