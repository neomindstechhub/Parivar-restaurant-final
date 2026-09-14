# Parivar Restaurant OS

A modern, full-stack restaurant operating system powering both the customer-facing digital ordering experience and back-of-house operations.

- **Public Ordering Site** — Interactive menu browsing, dine-in and takeaway ordering, add-on recommendations, table selection, and real-time live order tracking via WebSockets.
- **Admin Command Center (`/admin`)** — Real-time kitchen display queue, interactive table floor plan, billing and receipt generation, menu and category catalog management, catering requests, and role-based staff access.

---

## 🏗️ Architecture & Deployment

| Component | Technology | Hosting / Platform | Production Domain | Fallback / Staging Domain |
|---|---|---|---|---|
| **Frontend** | React 19, TanStack Start, Vite 7, Nitro, Tailwind CSS | **Vercel** | `https://parivar.restaurant` | `https://parivar-restaurant-gamma.vercel.app` (or `-final`) |
| **Backend** | Python 3.12, FastAPI, Uvicorn, WebSockets, SQLAlchemy (Async) | **Render** (Web Service) | `https://api.parivar.restaurant` | `https://parivar-restaurant-backend.onrender.com` (or `-final`) |
| **Database** | PostgreSQL 16+ (Serverless) | **Neon** | Direct AWS endpoint (`ap-southeast-2`) | Local SQLite (`parivar.db`) |

> [!NOTE]
> **Why Dual Deployment?**
> The backend runs as a persistent service on Render rather than Vercel Serverless to provide native support for **persistent WebSockets** (real-time order and kitchen queues) and unconstrained background worker tasks.

---

## 💻 Local Development Setup

### Prerequisites
- **Node.js 20+** and **npm** (uses `package-lock.json`)
- **Python 3.12** (must be 3.12 for pre-compiled binary wheel support)

---

### Step 1: Backend Setup (FastAPI + SQLite)

Open a terminal and run:

```bash
cd backend

# Create and activate Python virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Seed the local database (creates super admin and tables T01-T10)
python seed.py

# Start the local development server
uvicorn app.main:app --reload --port 8000
```

- **API Base**: `http://localhost:8000`
- **Interactive Swagger Docs**: `http://localhost:8000/docs`
- **WebSocket Endpoint**: `ws://localhost:8000/ws`
- **Default Super Admin**: `admin` / `admin123`

---

### Step 2: Frontend Setup (TanStack Start / Vite)

In a second terminal window (from the repository root):

```bash
# Install dependencies (flag required for React 19 peer dependencies)
npm install --legacy-peer-deps

# Start Vite dev server
npm run dev
```

- **Frontend App**: `http://localhost:8080` (or `http://localhost:5173`)
- **Admin Dashboard**: `http://localhost:8080/admin`

> [!TIP]
> In local development, the frontend automatically falls back to `http://localhost:8000` and `ws://localhost:8000` if environment variables are not set. No `.env` is required for local dev.

---

## 🚀 Production Deployment Settings

### 1. Frontend (Vercel)

- **Framework Preset**: `Vite` (defined in `vercel.json`)
- **Root Directory**: `./` (Repository root)
- **Install Command**: `npm install --legacy-peer-deps`
- **Build Command**: `npm run build`
- **Output Directory**: Default / leave empty (Nitro's Vercel preset emits `.vercel/output`)

#### Environment Variables (Vercel Dashboard):
```ini
VITE_API_URL=https://api.parivar.restaurant
VITE_WS_URL=wss://api.parivar.restaurant
```
*(CRITICAL: Do **not** append `/api/v1` to `VITE_API_URL` or `/ws` to `VITE_WS_URL`. The frontend appends these paths automatically.)*

---

### 2. Backend (Render)

- **Service Type**: `Web Service`
- **Runtime**: `Python`
- **Root Directory**: `backend` *(CRITICAL)*
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

#### Environment Variables (Render Dashboard):

| Variable | Recommended Value | Description |
|---|---|---|
| `PYTHON_VERSION` | `3.12.10` | **Mandatory**. Prevents Render defaulting to 3.13 (which breaks `cryptography`/`bcrypt` wheels). |
| `DATABASE_URL` | `postgresql+asyncpg://<user>:<password>@<host>/<dbname>` | Neon direct connection string (see below). |
| `SECRET_KEY` | *(Random 32+ character string)* | Used for JWT authentication signing. |
| `ALGORITHM` | `HS256` | JWT signing algorithm. |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `10080` | Session lifetime (7 days). |
| `CORS_ORIGINS` | `https://parivar.restaurant,https://www.parivar.restaurant,http://localhost:5173` | Allowed frontend origins without trailing slashes. |

#### Neon PostgreSQL Connection Format:
When copying the connection URI from Neon:
1. Replace `postgresql://` with `postgresql+asyncpg://`
2. Use the **Direct (non-pooler)** endpoint (e.g. `ep-example.ap-southeast-2.aws.neon.tech`)
3. Strip `?sslmode=require` from the end (SQLAlchemy passes `connect_args={"ssl": "require"}` automatically)

#### First-Time Database Seeding (Production):
Run `python seed.py` once via Render's Web Shell to seed the `admin` account and initial tables. The main menu and specials are auto-seeded on application startup.

---

## 🧪 Deployment Verification

This repository includes an automated verification script to test backend health, CORS headers, and menu data:

```bash
# Test active production deployment:
python3 scripts/verify_deployment.py --backend https://api.parivar.restaurant --frontend https://parivar.restaurant

# Test default/fallback deployment:
python3 scripts/verify_deployment.py
```

---

## 📁 Repository Layout

```
├── backend/                  # FastAPI backend application
│   ├── app/
│   │   ├── core/             # Auth, settings, websockets
│   │   ├── database/         # SQLAlchemy models, engine, schemas
│   │   └── modules/          # Menu, categories, orders, tables, kitchen, billing
│   ├── requirements.txt      # Pinned backend dependencies
│   └── seed.py               # Database seeder (admin user & floor tables)
├── public/                   # Static frontend assets
│   ├── frames/               # Hero animation webp frames
│   └── menu-images/          # Public menu catalog images
├── scripts/
│   ├── extract-frames.mjs    # Video frame extractor utility
│   └── verify_deployment.py  # Production deployment health and CORS validator
├── src/                      # TanStack Start frontend application
│   ├── components/           # UI components (Hero, CartDrawer, Navbar, Admin views)
│   ├── routes/               # TanStack file-based routes
│   └── utils/                # Image resolution & API helpers
├── render.yaml               # Render Infrastructure-as-Code blueprint
├── vercel.json               # Vercel SPA rewrites, headers, and build config
└── vite.config.ts            # Vite + TanStack Start + Nitro config
```

---

## ⚠️ Important Rules & Gotchas

1. **URL Concatenation in Frontend**: Every API call appends `'/api/v1/...'` to `VITE_API_URL`. Never configure `VITE_API_URL` with `/api/v1`.
2. **WebSocket URL Concatenation**: `useWebSocket.ts` appends `'/ws'` to `VITE_WS_URL`. Never configure `VITE_WS_URL` with `/ws`.
3. **CORS Configuration**: `CORS_ORIGINS` on Render must include the exact frontend origin(s) with no trailing slash. Never use `"*"` in production.
4. **Local Image Backups**: Raw uncompressed images are preserved in `menu-images.local/` (gitignored) to keep repository deployments fast and lightweight.
