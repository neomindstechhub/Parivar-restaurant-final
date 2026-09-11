from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import json
from pathlib import Path
from app.core.config import settings
from app.core.config import settings
from app.core.websockets import manager
from app.database.database import engine, Base
from app.database import models
from app.modules.menu.router import router as menu_router
from app.modules.categories.router import router as category_router
from app.modules.auth.router import router as auth_router
from app.modules.tables.router import router as tables_router
from app.modules.orders.router import router as orders_router
from app.modules.kitchen.router import router as kitchen_router
from app.modules.payments.router import router as payments_router
from app.modules.users.router import router as users_router
from app.modules.catering.router import router as catering_router
from app.modules.uploads.router import router as uploads_router
from app.seed_extras import seed_addons_and_specials, seed_main_menu

UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(",") if settings.CORS_ORIGINS != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(users_router, prefix=f"{settings.API_V1_STR}/users")
app.include_router(menu_router, prefix=f"{settings.API_V1_STR}/menu")
app.include_router(category_router, prefix=f"{settings.API_V1_STR}/categories")
app.include_router(tables_router, prefix=settings.API_V1_STR)
app.include_router(orders_router, prefix=settings.API_V1_STR)
app.include_router(kitchen_router, prefix=settings.API_V1_STR)
app.include_router(payments_router, prefix=settings.API_V1_STR)
app.include_router(catering_router, prefix=settings.API_V1_STR)
app.include_router(uploads_router, prefix=f"{settings.API_V1_STR}/uploads", tags=["uploads"])
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

@app.on_event("startup")
async def on_startup():
    await init_models()
    await seed_addons_and_specials()
    await seed_main_menu()

@app.get("/")
def read_root():
    return {"message": "Welcome to Parivar Restaurant OS API"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                if message.get("type") == "PING":
                    await websocket.send_text(json.dumps({"type": "PONG"}))
            except json.JSONDecodeError:
                pass
    except WebSocketDisconnect:
        manager.disconnect(websocket)
