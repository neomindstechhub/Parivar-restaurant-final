import asyncio
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import engine, Base, AsyncSessionLocal
from app.database import models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Menu data from frontend
menuData = {
  "Entrée": [
    { "name": "Tandoori (Half)", "desc": "Tandoori (Half)", "price": 11.99, "img": "/src/assets/parivar-logo.png" },
    { "name": "Tandoori (Full)", "desc": "Tandoori (Full)", "price": 17.99, "img": "/src/assets/parivar-logo.png" },
    { "name": "Chicken Tikka", "desc": "Chicken Tikka", "price": 14.99, "img": "/src/assets/parivar-logo.png" },
    { "name": "Sheekh Kebab", "desc": "Sheekh Kebab", "price": 13.99, "img": "/src/assets/parivar-logo.png" },
    { "name": "Fish Fry (Basa)", "desc": "Fish Fry (Basa)", "price": 14.99, "img": "/src/assets/parivar-logo.png" },
    { "name": "Chicken 65", "desc": "Chicken 65", "price": 14.99, "img": "/src/assets/parivar-logo.png" },
    { "name": "Mutton Haleem", "desc": "Mutton Haleem", "price": 14.99, "img": "/src/assets/parivar-logo.png" },
  ],
  "Naan Bread": [
    { "name": "Plain Naan", "desc": "Plain Naan", "price": 2.00, "img": "/src/assets/parivar-logo.png" },
    { "name": "Butter Naan", "desc": "Butter Naan", "price": 3.00, "img": "/src/assets/parivar-logo.png" },
    { "name": "Garlic Naan", "desc": "Garlic Naan", "price": 3.50, "img": "/src/assets/parivar-logo.png" },
  ],
  "Savory Items": [
    { "name": "Momos (10 pcs)", "desc": "Momos (10 pcs)", "price": 11.99, "img": "/src/assets/parivar-logo.png" },
    { "name": "Samosa (2 pcs)", "desc": "Samosa (2 pcs)", "price": 4.99, "img": "/src/assets/parivar-logo.png" },
    { "name": "Vegetable Roll", "desc": "Vegetable Roll", "price": 2.50, "img": "/src/assets/parivar-logo.png" },
  ],
  "Chicken Curries": [
    { "name": "Butter Chicken", "desc": "Butter Chicken", "price": 14.99, "img": "/src/assets/parivar-logo.png" },
    { "name": "Achari Chicken", "desc": "Achari Chicken", "price": 14.99, "img": "/src/assets/parivar-logo.png" },
    { "name": "Chicken Khorma", "desc": "Chicken Khorma", "price": 13.99, "img": "/src/assets/parivar-logo.png" },
    { "name": "Parivar Special Chicken Gravy", "desc": "Parivar Special Chicken Gravy", "price": 14.99, "img": "/src/assets/parivar-logo.png" },
    { "name": "Chicken Vindaloo", "desc": "Chicken Vindaloo", "price": 13.99, "img": "/src/assets/parivar-logo.png" },
    { "name": "Chicken Masala", "desc": "Chicken Masala", "price": 14.99, "img": "/src/assets/parivar-logo.png" },
  ],
  "Mutton Curries": [
    { "name": "Mutton Vindaloo", "desc": "Mutton Vindaloo", "price": 14.99, "img": "/src/assets/parivar-logo.png" },
    { "name": "Mutton Khorma", "desc": "Mutton Khorma", "price": 14.99, "img": "/src/assets/parivar-logo.png" },
    { "name": "Mutton Masala", "desc": "Mutton Masala", "price": 14.99, "img": "/src/assets/parivar-logo.png" },
  ],
  "Vegetarian Curries": [
    { "name": "Daal Tadka", "desc": "Daal Tadka", "price": 11.99, "img": "/src/assets/parivar-logo.png" },
    { "name": "Mixed Veg Curry", "desc": "Mixed Veg Curry", "price": 13.99, "img": "/src/assets/parivar-logo.png" },
    { "name": "Paneer Tikka Masala", "desc": "Paneer Tikka Masala", "price": 13.99, "img": "/src/assets/parivar-logo.png" },
  ],
  "Desi Chinese": [
    { "name": "Chicken Fry Noodles", "desc": "Chicken Fry Noodles", "price": 14.99, "img": "/src/assets/parivar-logo.png" },
    { "name": "Veg Fry Noodles", "desc": "Veg Fry Noodles", "price": 12.99, "img": "/src/assets/parivar-logo.png" },
    { "name": "Chicken Manchurian", "desc": "Chicken Manchurian", "price": 14.99, "img": "/src/assets/parivar-logo.png" },
    { "name": "Veg Manchurian", "desc": "Veg Manchurian", "price": 13.99, "img": "/src/assets/parivar-logo.png" },
    { "name": "Chicken Fried Rice", "desc": "Chicken Fried Rice", "price": 14.99, "img": "/src/assets/parivar-logo.png" },
    { "name": "Veg Fried Rice", "desc": "Veg Fried Rice", "price": 12.99, "img": "/src/assets/parivar-logo.png" },
  ],
  "Deals": [
    { "name": "Deal 1", "desc": "Khorma (Mutton/Lamb) + Saffron Rice", "price": 15.99, "img": "/src/assets/parivar-logo.png" },
    { "name": "Deal 2", "desc": "Butter Chicken + 2 Butter Naan", "price": 17.99, "img": "/src/assets/parivar-logo.png" },
    { "name": "Deal 3", "desc": "Momos (10 pcs) + Mango Lassi/Can Drink", "price": 14.99, "img": "/src/assets/parivar-logo.png" },
    { "name": "Deal 4", "desc": "Sheekh Kebab (1 Skewer) + Naan (1 pc)", "price": 16.99, "img": "/src/assets/parivar-logo.png" },
    { "name": "Deal 5", "desc": "Chicken 65 + Rice + Daal", "price": 15.00, "img": "/src/assets/parivar-logo.png" },
    { "name": "Deal 6", "desc": "Vindaloo (Chicken/Lamb) + Saffron Rice", "price": 16.99, "img": "/src/assets/parivar-logo.png" },
  ],
  "Platter Deals": [
    { "name": "Platter Deal 1 (For 2)", "desc": "Half Tandoori OR Chicken Tikka Kebab • Fish Fry OR Chicken Momo • Chicken 65 • 2 Naan • Mint Chutney", "price": 38.00, "img": "/src/assets/parivar-logo.png" },
    { "name": "Platter Deal 2 (For 3)", "desc": "Half Tandoori • Chicken Tikka Kebab OR Lamb Sheekh Kebab • Fish Fry OR Prawn Fry • Chicken 65 • 3 Naan • Mint Chutney", "price": 48.00, "img": "/src/assets/parivar-logo.png" },
    { "name": "Platter Deal 3 (For 4)", "desc": "Full Tandoori OR Chicken Sheekh Kebab OR Lamb Sheekh Kebab (2 Skewers) • Chicken Momo • Fish Fry OR Prawn Fry • Chicken 65 OR Parivar Special Chicken Curry • 4 Naan OR 2 Saffron Rice • Mint Chutney", "price": 75.00, "img": "/src/assets/parivar-logo.png" },
  ],
  "Desserts": [
    { "name": "Gulab Jamun", "desc": "Gulab Jamun", "price": 4.99, "img": "/src/assets/parivar-logo.png" },
    { "name": "Qubani", "desc": "Qubani", "price": 4.99, "img": "/src/assets/parivar-logo.png" },
    { "name": "Rasmalai", "desc": "Rasmalai", "price": 4.99, "img": "/src/assets/parivar-logo.png" },
    { "name": "Shahi Tukda", "desc": "Shahi Tukda", "price": 4.99, "img": "/src/assets/parivar-logo.png" },
    { "name": "Zafrani Kheer", "desc": "Zafrani Kheer", "price": 4.99, "img": "/src/assets/parivar-logo.png" },
    { "name": "Khowa Puri", "desc": "Khowa Puri", "price": 4.99, "img": "/src/assets/parivar-logo.png" },
  ],
  "Drinks": [
    { "name": "Chai Small", "desc": "Chai Small", "price": 1.99, "img": "/src/assets/parivar-logo.png" },
    { "name": "Chai Large", "desc": "Chai Large", "price": 2.99, "img": "/src/assets/parivar-logo.png" },
    { "name": "Mango Lassi", "desc": "Mango Lassi", "price": 3.99, "img": "/src/assets/parivar-logo.png" },
    { "name": "Can Drink", "desc": "Can Drink", "price": 2.50, "img": "/src/assets/parivar-logo.png" },
    { "name": "Water Bottle", "desc": "Water Bottle", "price": 1.00, "img": "/src/assets/parivar-logo.png" },
  ],
}

category_images = {
  "Entrée": "/src/assets/parivar-logo.png",
  "Naan Bread": "/src/assets/parivar-logo.png",
  "Savory Items": "/src/assets/parivar-logo.png",
  "Chicken Curries": "/src/assets/parivar-logo.png",
  "Mutton Curries": "/src/assets/parivar-logo.png",
  "Vegetarian Curries": "/src/assets/parivar-logo.png",
  "Desi Chinese": "/src/assets/parivar-logo.png",
  "Deals": "/src/assets/parivar-logo.png",
  "Platter Deals": "/src/assets/parivar-logo.png",
  "Desserts": "/src/assets/parivar-logo.png",
  "Drinks": "/src/assets/parivar-logo.png"
}

async def seed_data():
    logger.info("Initializing database...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("Seeding data...")
    async with AsyncSessionLocal() as session:
        # Skip the placeholder menu catalog if any category already exists
        # (seed_extras.py auto-seeds "Add-ons"/"Today's Special" on every
        # startup) - but admin/table seeding below must still run regardless,
        # since each has its own idempotency check.
        from sqlalchemy import select
        result = await session.execute(select(models.Category))
        if result.scalars().first():
            logger.info("Categories already exist, skipping placeholder menu seed.")
        else:
            for cat_name, items in menuData.items():
                cat = models.Category(
                    name=cat_name,
                    description=f"Authentic {cat_name}",
                    image_url=category_images.get(cat_name)
                )
                session.add(cat)
                await session.commit()
                await session.refresh(cat)

                for item in items:
                    menu_item = models.MenuItem(
                        category_id=cat.id,
                        name=item["name"],
                        description=item["desc"],
                        price=item["price"],
                        image_url=item["img"]
                    )
                    session.add(menu_item)

                await session.commit()

        # Seed Super Admin User
        result = await session.execute(select(models.User).where(models.User.username == "admin"))
        if not result.scalars().first():
            import bcrypt
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw("admin123".encode('utf-8'), salt).decode('utf-8')
            
            admin_user = models.User(
                username="admin",
                password_hash=hashed_password,
                role=models.UserRole.SUPER_ADMIN,
                is_active=True
            )
            session.add(admin_user)
            await session.commit()
            logger.info("Seeded Admin user (admin / admin123)")

        # Seed Mock Tables
        result = await session.execute(select(models.RestaurantTable))
        if not result.scalars().first():
            for i in range(1, 11):
                table = models.RestaurantTable(
                    table_number=f"T{i:02d}",
                    status=models.TableStatus.AVAILABLE,
                    capacity=4 if i < 9 else 8
                )
                session.add(table)
            await session.commit()
            logger.info("Seeded 10 Mock Tables")

    logger.info("Seeding complete.")

if __name__ == "__main__":
    async def run():
        await seed_data()
        from app.seed_extras import seed_addons_and_specials
        await seed_addons_and_specials()
    asyncio.run(run())
