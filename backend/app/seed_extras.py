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
    {"name": "Chef's Dum Biryani", "desc": "Today's slow-cooked lamb biryani with saffron rice", "price": 18.99, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787056264/2_jlzkle.jpg"},
    {"name": "Royal Haleem Bowl", "desc": "Limited batch heritage haleem — only today", "price": 14.99, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787056130/1_g8gsoo.jpg"},
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
        {"name": "Sheekh Kebab", "desc": "Minced meat skewers with aromatic spices", "price": 13.99, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787056642/8_nodyar.webp"},
        {"name": "Fish Fry (Basa)", "desc": "Crispy fried basa fish with spices", "price": 14.99, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787056736/7_csyno8.avif"},
        {"name": "Chicken 65", "desc": "Spicy deep-fried chicken bites", "price": 14.99, "img": "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?q=80&w=800&auto=format&fit=crop"},
        {"name": "Mutton Haleem", "desc": "Slow-cooked lentil and meat stew", "price": 14.99, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787056130/1_g8gsoo.jpg"},
    ],
    "Naan Bread": [
        {"name": "Plain Naan", "desc": "Soft, freshly baked naan bread", "price": 2.00, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787056843/9_r61oag.jpg"},
        {"name": "Butter Naan", "desc": "Naan brushed with melted butter", "price": 3.00, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787056843/9_r61oag.jpg"},
        {"name": "Garlic Naan", "desc": "Naan topped with fresh garlic and herbs", "price": 3.50, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787057000/11_tcqqht.jpg"},
    ],
    "Savory Items": [
        {"name": "Momos (10 pcs)", "desc": "Steamed dumplings with dipping sauce", "price": 11.99, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787056464/5_il90qp.jpg"},
        {"name": "Samosa (2 pcs)", "desc": "Crispy pastry filled with spiced potatoes", "price": 4.99, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787056419/4_ldlbhe.jpg"},
        {"name": "Vegetable Roll", "desc": "Flaky roll stuffed with seasoned vegetables", "price": 2.50, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787056575/6_pkmebp.webp"},
    ],
    "Chicken Curries": [
        {"name": "Butter Chicken", "desc": "Classic creamy tomato curry, mildly spiced", "price": 14.99, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787057584/17_agl38c.avif"},
        {"name": "Achari Chicken", "desc": "Chicken in tangy pickle-spiced gravy", "price": 14.99, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787057584/17_agl38c.avif"},
        {"name": "Chicken Khorma", "desc": "Mild, creamy chicken in cashew sauce", "price": 13.99, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787058411/19_e1eowg.jpg"},
        {"name": "Parivar Special Chicken Gravy", "desc": "Our signature chicken curry recipe", "price": 14.99, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787058495/20_o5npca.jpg"},
        {"name": "Chicken Vindaloo", "desc": "Fiery Goan-style chicken curry", "price": 13.99, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787058550/21_jlbc5b.jpg"},
        {"name": "Chicken Masala", "desc": "Rich and spiced chicken masala gravy", "price": 14.99, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787058665/22_vwwqxh.jpg"},
    ],
    "Mutton Curries": [
        {"name": "Mutton Vindaloo", "desc": "Spicy vindaloo with tender mutton", "price": 14.99, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787058733/23_en28o5.jpg"},
        {"name": "Mutton Khorma", "desc": "Creamy mutton in aromatic korma sauce", "price": 14.99, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787058789/24_ghxkbz.jpg"},
        {"name": "Mutton Masala", "desc": "Bold and flavorful mutton masala curry", "price": 14.99, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787058849/25_tieqqj.jpg"},
    ],
    "Vegetarian Curries": [
        {"name": "Daal Tadka", "desc": "Yellow lentils tempered with garlic and spices", "price": 11.99, "img": "https://images.unsplash.com/photo-1626509646543-518ee55030e4?q=80&w=800&auto=format&fit=crop"},
        {"name": "Mixed Veg Curry", "desc": "Seasonal vegetables in a rich gravy", "price": 13.99, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787058912/26_r6jiaw.jpg"},
        {"name": "Paneer Tikka Masala", "desc": "Grilled paneer in spiced tomato sauce", "price": 13.99, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787058969/27_xsldjd.jpg"},
    ],
    "Desi Chinese": [
        {"name": "Chicken Fry Noodles", "desc": "Stir-fried noodles with chicken", "price": 14.99, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787059055/28_eukwyi.jpg"},
        {"name": "Veg Fry Noodles", "desc": "Stir-fried noodles with vegetables", "price": 12.99, "img": "https://images.unsplash.com/photo-1512621843614-b4bf72d1f0d3?q=80&w=800&auto=format&fit=crop"},
        {"name": "Chicken Manchurian", "desc": "Indo-Chinese chicken in tangy sauce", "price": 14.99, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787059101/29_tkbtxd.webp"},
        {"name": "Veg Manchurian", "desc": "Vegetable balls in Manchurian sauce", "price": 13.99, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787059155/30_gyryht.jpg"},
        {"name": "Chicken Fried Rice", "desc": "Wok-tossed rice with chicken and vegetables", "price": 14.99, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787059215/31_hzkkzs.webp"},
        {"name": "Veg Fried Rice", "desc": "Wok-tossed rice with fresh vegetables", "price": 12.99, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787059285/32_glqnri.jpg"},
    ],
    "Desserts": [
        {"name": "Gulab Jamun", "desc": "Golden fried milk dumplings in syrup", "price": 4.99, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787059366/33_jmmded.jpg"},
        {"name": "Qubani", "desc": "Stewed apricot dessert with cream", "price": 4.99, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787059429/34_lef3g3.jpg"},
        {"name": "Rasmalai", "desc": "Soft paneer discs in sweetened milk", "price": 4.99, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787059516/35_c6byxv.jpg"},
        {"name": "Shahi Tukda", "desc": "Fried bread soaked in saffron milk and nuts", "price": 4.99, "img": "https://images.unsplash.com/photo-1551024506-0bccd828d307?q=80&w=800&auto=format&fit=crop"},
        {"name": "Zafrani Kheer", "desc": "Saffron-infused rice pudding", "price": 4.99, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787059576/36_ipydit.jpg"},
        {"name": "Khowa Puri", "desc": "Sweet fried bread with thickened milk filling", "price": 4.99, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787059662/37_ms78sj.jpg"},
    ],
    "Drinks": [
        {"name": "Chai Small", "desc": "Authentic spiced Indian tea", "price": 1.99, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787057104/12_cmt01s.jpg"},
        {"name": "Chai Large", "desc": "Large cup of spiced Indian tea", "price": 2.99, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787057248/13_cj1ec7.jpg"},
        {"name": "Mango Lassi", "desc": "Sweet, rich yogurt drink with mango", "price": 3.99, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787057298/14_aj7lb2.jpg"},
        {"name": "Can Drink", "desc": "Assorted canned beverages", "price": 2.50, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787057522/16_a83b5q.jpg"},
        {"name": "Water Bottle", "desc": "Purified drinking water", "price": 1.00, "img": "https://res.cloudinary.com/akmdvmmw/image/upload/v1787057451/15_ehvwx6.jpg"},
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
