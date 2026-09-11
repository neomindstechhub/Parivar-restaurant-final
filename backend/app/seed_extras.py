import logging
from sqlalchemy import select
from app.database.database import AsyncSessionLocal
from app.database import models

logger = logging.getLogger(__name__)

ADDON_ITEMS = [
    {"name": "Extra Butter Naan", "desc": "Add an extra butter naan to your meal", "price": 3.00, "img": "/menu-images/Naan Bread/butter naan.png"},
    {"name": "Extra Garlic Naan", "desc": "Garlic naan on the side", "price": 3.50, "img": "/menu-images/Naan Bread/garlic naan.png"},
    {"name": "Raita", "desc": "Cooling yogurt with cucumber and mint", "price": 2.50, "img": "/menu-images/Savory Items/momos 10 pcs.png"},
    {"name": "Extra Rice", "desc": "Steamed saffron basmati rice", "price": 3.00, "img": "/menu-images/Desi Chinese/veg fried rice.png"},
    {"name": "Mint Chutney", "desc": "Fresh mint and coriander chutney", "price": 1.50, "img": "/menu-images/Savory Items/samosa 2 pcs.png"},
    {"name": "Papadum (2 pcs)", "desc": "Crispy lentil wafers", "price": 2.00, "img": "/menu-images/Savory Items/samosa 2 pcs.png"},
]

SPECIAL_ITEMS = [
    {"name": "Chef's Dum Biryani", "desc": "Today's slow-cooked lamb biryani with saffron rice", "price": 18.99, "img": "/menu-images/Desi Chinese/chicken fried  rice.png"},
    {"name": "Royal Haleem Bowl", "desc": "Limited batch heritage haleem — only today", "price": 14.99, "img": "/menu-images/Entree/mutton haleem.png"},
    {"name": "Tandoori Platter Special", "desc": "Mixed grill with naan and chutney — today's deal", "price": 22.99, "img": "/menu-images/Entree/tandoor (full).png"},
]

# Mirrors src/routes/menu.tsx's fallbackMenuData exactly (names, descriptions,
# prices, image URLs) so items the frontend shows are always orderable -
# without this, the frontend silently falls back to this same data client-side
# when a category has no backend items, but those mock items don't exist as
# real MenuItem rows and fail with a 400 on checkout.
MAIN_MENU = {
    "Entrée": [
        {"name": "Tandoori (Half)", "desc": "Half tandoori chicken, marinated and charred", "price": 11.99, "img": "https://images.unsplash.com/photo-1610057099431-d73a1c9d2f2f?q=80&w=800&auto=format&fit=crop"},
        {"name": "Tandoori (Full)", "desc": "Full tandoori chicken, smoky and juicy", "price": 17.99, "img": "https://images.unsplash.com/photo-1599487405902-1823ebce1711?q=80&w=800&auto=format&fit=crop"},
        {"name": "Chicken Tikka", "desc": "Boneless chicken pieces, spiced and grilled", "price": 14.99, "img": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?q=80&w=800&auto=format&fit=crop"},
        {"name": "Sheekh Kebab", "desc": "Minced meat skewers with aromatic spices", "price": 13.99, "img": "https://images.unsplash.com/photo-1544025162-d76694265947?q=80&w=800&auto=format&fit=crop"},
        {"name": "Fish Fry (Basa)", "desc": "Crispy fried basa fish with spices", "price": 14.99, "img": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?q=80&w=800&auto=format&fit=crop"},
        {"name": "Chicken 65", "desc": "Spicy deep-fried chicken bites", "price": 14.99, "img": "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?q=80&w=800&auto=format&fit=crop"},
        {"name": "Mutton Haleem", "desc": "Slow-cooked lentil and meat stew", "price": 14.99, "img": "https://images.unsplash.com/photo-1548943487-a2e4e43b4859?q=80&w=800&auto=format&fit=crop"},
    ],
    "Naan Bread": [
        {"name": "Plain Naan", "desc": "Soft, freshly baked naan bread", "price": 2.00, "img": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?q=80&w=800&auto=format&fit=crop"},
        {"name": "Butter Naan", "desc": "Naan brushed with melted butter", "price": 3.00, "img": "https://images.unsplash.com/photo-1599487405902-1823ebce1711?q=80&w=800&auto=format&fit=crop"},
        {"name": "Garlic Naan", "desc": "Naan topped with fresh garlic and herbs", "price": 3.50, "img": "https://images.unsplash.com/photo-1610057099431-d73a1c9d2f2f?q=80&w=800&auto=format&fit=crop"},
    ],
    "Savory Items": [
        {"name": "Momos (10 pcs)", "desc": "Steamed dumplings with dipping sauce", "price": 11.99, "img": "https://images.unsplash.com/photo-1626509646543-518ee55030e4?q=80&w=800&auto=format&fit=crop"},
        {"name": "Samosa (2 pcs)", "desc": "Crispy pastry filled with spiced potatoes", "price": 4.99, "img": "https://images.unsplash.com/photo-1601050690597-df0568f70950?q=80&w=800&auto=format&fit=crop"},
        {"name": "Vegetable Roll", "desc": "Flaky roll stuffed with seasoned vegetables", "price": 2.50, "img": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?q=80&w=800&auto=format&fit=crop"},
    ],
    "Chicken Curries": [
        {"name": "Butter Chicken", "desc": "Classic creamy tomato curry, mildly spiced", "price": 14.99, "img": "https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?q=80&w=800&auto=format&fit=crop"},
        {"name": "Achari Chicken", "desc": "Chicken in tangy pickle-spiced gravy", "price": 14.99, "img": "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?q=80&w=800&auto=format&fit=crop"},
        {"name": "Chicken Khorma", "desc": "Mild, creamy chicken in cashew sauce", "price": 13.99, "img": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?q=80&w=800&auto=format&fit=crop"},
        {"name": "Parivar Special Chicken Gravy", "desc": "Our signature chicken curry recipe", "price": 14.99, "img": "https://images.unsplash.com/photo-1599487405902-1823ebce1711?q=80&w=800&auto=format&fit=crop"},
        {"name": "Chicken Vindaloo", "desc": "Fiery Goan-style chicken curry", "price": 13.99, "img": "https://images.unsplash.com/photo-1610057099431-d73a1c9d2f2f?q=80&w=800&auto=format&fit=crop"},
        {"name": "Chicken Masala", "desc": "Rich and spiced chicken masala gravy", "price": 14.99, "img": "https://images.unsplash.com/photo-1544025162-d76694265947?q=80&w=800&auto=format&fit=crop"},
    ],
    "Mutton Curries": [
        {"name": "Mutton Vindaloo", "desc": "Spicy vindaloo with tender mutton", "price": 14.99, "img": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?q=80&w=800&auto=format&fit=crop"},
        {"name": "Mutton Khorma", "desc": "Creamy mutton in aromatic korma sauce", "price": 14.99, "img": "https://images.unsplash.com/photo-1548943487-a2e4e43b4859?q=80&w=800&auto=format&fit=crop"},
        {"name": "Mutton Masala", "desc": "Bold and flavorful mutton masala curry", "price": 14.99, "img": "https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?q=80&w=800&auto=format&fit=crop"},
    ],
    "Vegetarian Curries": [
        {"name": "Daal Tadka", "desc": "Yellow lentils tempered with garlic and spices", "price": 11.99, "img": "https://images.unsplash.com/photo-1626509646543-518ee55030e4?q=80&w=800&auto=format&fit=crop"},
        {"name": "Mixed Veg Curry", "desc": "Seasonal vegetables in a rich gravy", "price": 13.99, "img": "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?q=80&w=800&auto=format&fit=crop"},
        {"name": "Paneer Tikka Masala", "desc": "Grilled paneer in spiced tomato sauce", "price": 13.99, "img": "https://images.unsplash.com/photo-1599487405902-1823ebce1711?q=80&w=800&auto=format&fit=crop"},
    ],
    "Desi Chinese": [
        {"name": "Chicken Fry Noodles", "desc": "Stir-fried noodles with chicken", "price": 14.99, "img": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?q=80&w=800&auto=format&fit=crop"},
        {"name": "Veg Fry Noodles", "desc": "Stir-fried noodles with vegetables", "price": 12.99, "img": "https://images.unsplash.com/photo-1512621843614-b4bf72d1f0d3?q=80&w=800&auto=format&fit=crop"},
        {"name": "Chicken Manchurian", "desc": "Indo-Chinese chicken in tangy sauce", "price": 14.99, "img": "https://images.unsplash.com/photo-1544025162-d76694265947?q=80&w=800&auto=format&fit=crop"},
        {"name": "Veg Manchurian", "desc": "Vegetable balls in Manchurian sauce", "price": 13.99, "img": "https://images.unsplash.com/photo-1626509646543-518ee55030e4?q=80&w=800&auto=format&fit=crop"},
        {"name": "Chicken Fried Rice", "desc": "Wok-tossed rice with chicken and vegetables", "price": 14.99, "img": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?q=80&w=800&auto=format&fit=crop"},
        {"name": "Veg Fried Rice", "desc": "Wok-tossed rice with fresh vegetables", "price": 12.99, "img": "https://images.unsplash.com/photo-1512621843614-b4bf72d1f0d3?q=80&w=800&auto=format&fit=crop"},
    ],
    "Desserts": [
        {"name": "Gulab Jamun", "desc": "Golden fried milk dumplings in syrup", "price": 4.99, "img": "https://images.unsplash.com/photo-1601050690597-df0568f70950?q=80&w=800&auto=format&fit=crop"},
        {"name": "Qubani", "desc": "Stewed apricot dessert with cream", "price": 4.99, "img": "https://images.unsplash.com/photo-1551024506-0bccd828d307?q=80&w=800&auto=format&fit=crop"},
        {"name": "Rasmalai", "desc": "Soft paneer discs in sweetened milk", "price": 4.99, "img": "https://images.unsplash.com/photo-1601050690597-df0568f70950?q=80&w=800&auto=format&fit=crop"},
        {"name": "Shahi Tukda", "desc": "Fried bread soaked in saffron milk and nuts", "price": 4.99, "img": "https://images.unsplash.com/photo-1551024506-0bccd828d307?q=80&w=800&auto=format&fit=crop"},
        {"name": "Zafrani Kheer", "desc": "Saffron-infused rice pudding", "price": 4.99, "img": "https://images.unsplash.com/photo-1601050690597-df0568f70950?q=80&w=800&auto=format&fit=crop"},
        {"name": "Khowa Puri", "desc": "Sweet fried bread with thickened milk filling", "price": 4.99, "img": "https://images.unsplash.com/photo-1551024506-0bccd828d307?q=80&w=800&auto=format&fit=crop"},
    ],
    "Drinks": [
        {"name": "Chai Small", "desc": "Authentic spiced Indian tea", "price": 1.99, "img": "https://images.unsplash.com/photo-1576092762791-dd9e2220afa1?q=80&w=800&auto=format&fit=crop"},
        {"name": "Chai Large", "desc": "Large cup of spiced Indian tea", "price": 2.99, "img": "https://images.unsplash.com/photo-1576092762791-dd9e2220afa1?q=80&w=800&auto=format&fit=crop"},
        {"name": "Mango Lassi", "desc": "Sweet, rich yogurt drink with mango", "price": 3.99, "img": "https://images.unsplash.com/photo-1546171753-97d7676e4602?q=80&w=800&auto=format&fit=crop"},
        {"name": "Can Drink", "desc": "Assorted canned beverages", "price": 2.50, "img": "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?q=80&w=800&auto=format&fit=crop"},
        {"name": "Water Bottle", "desc": "Purified drinking water", "price": 1.00, "img": "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?q=80&w=800&auto=format&fit=crop"},
    ],
}


async def _seed_category(session, cat_name, items, desc, cat_image="/src/assets/parivar-logo.png"):
    result = await session.execute(select(models.Category).where(models.Category.name == cat_name))
    cat = result.scalars().first()
    if not cat:
        cat = models.Category(name=cat_name, description=desc, image_url=cat_image)
        session.add(cat)
        await session.commit()
        await session.refresh(cat)
        logger.info("Created category: %s", cat_name)

    for item in items:
        existing = await session.execute(
            select(models.MenuItem).where(
                models.MenuItem.category_id == cat.id,
                models.MenuItem.name == item["name"],
            )
        )
        if not existing.scalars().first():
            session.add(models.MenuItem(
                category_id=cat.id,
                name=item["name"],
                description=item["desc"],
                price=item["price"],
                image_url=item["img"],
                is_available=True,
            ))
    await session.commit()


async def seed_addons_and_specials():
    async with AsyncSessionLocal() as session:
        await _seed_category(session, "Add-ons", ADDON_ITEMS, "Extra items customers can add to their order")
        await _seed_category(session, "Today's Special", SPECIAL_ITEMS, "Featured dishes for today")


async def seed_main_menu():
    async with AsyncSessionLocal() as session:
        for cat_name, items in MAIN_MENU.items():
            await _seed_category(session, cat_name, items, f"Authentic {cat_name}", cat_image=items[0]["img"])
