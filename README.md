# Parivar Restaurant OS

A restaurant ordering + back-of-house system:

- **Public site** — browse the menu, place dine-in/takeaway orders, track
  order status live over WebSocket.
- **Admin "Command Center"** (`/admin`) — menu & category management, table
  floor plan, kitchen queue, billing/payments, catering requests, user
  management.

**Stack:** TanStack Start (React 19 + Vite 7, SSR via Nitro) on the frontend,
FastAPI + SQLAlchemy (async) + JWT auth on the backend.

For open issues, deployment status, and what's left before this is properly
live, see [`NEXT_STEPS.md`](./NEXT_STEPS.md) — that file tracks the current
punch list and goes stale faster than this one.

## Prerequisites

- **Node.js 20+** (developed against Node 24) and **npm** — the repo commits
  `package-lock.json`; use npm, not `bun` (a `bun.lock` also exists but isn't
  the one actually used to build/deploy).
- **Python 3.12+** for the backend. [`uv`](https://docs.astral.sh/uv/) is
  recommended — it can install and manage the Python version for you.

## Frontend setup

```bash
npm install
npm run dev       # http://localhost:8080 (Vite dev server)
npm run build     # production build (emits .vercel/output via Nitro's vercel preset)
npm run lint
npm test          # vitest
```

A root `.npmrc` sets `legacy-peer-deps=true` — one dev dependency
(`nitro`, pinned to a dated beta) doesn't cleanly satisfy npm's strict
peer-dependency resolution against `@lovable.dev/vite-tanstack-config`'s
declared range, even though the actual versions are compatible. This matches
what the Vercel build already does; without it, plain `npm install` fails.

Copy `.env.example` to `.env` and adjust for local dev:

```
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws
```

(Do **not** include `/api/v1` in `VITE_API_URL` — the frontend code appends
that itself on every call.)

## Backend setup

```bash
cd backend
uv venv .venv --python 3.12
uv pip install -r requirements.txt --python .venv
.venv/Scripts/python.exe -m uvicorn app.main:app --reload --port 8000   # Windows
# .venv/bin/python -m uvicorn app.main:app --reload --port 8000        # macOS/Linux
```

This creates/seeds a local `parivar.db` SQLite file on first run (see
`backend/seed.py`) and serves:
- API at `http://localhost:8000/api/v1/...`
- Interactive docs at `http://localhost:8000/docs`
- WebSocket at `ws://localhost:8000/ws`

Default env vars (see `.env.example` for the full list) fall back to local
SQLite and a dev `SECRET_KEY` if unset — fine for local dev, **must** be
overridden in any real deployment (a real `DATABASE_URL` pointing at
Postgres, a random `SECRET_KEY`, and `CORS_ORIGINS` set to your real
frontend domain — see `render.yaml` for the intended production shape).

A default admin account is seeded: `admin` / `admin123`. Change this before
any deployment goes live.

## Repo layout

```
src/            frontend (TanStack Start routes, components, state)
backend/        FastAPI app — the real backend (deploy target: Render + Postgres)
api/            the same FastAPI app repackaged as a Vercel serverless function
                (SQLite in /tmp — ephemeral, demo-only, not for real data)
public/         static assets (menu images, etc.)
```

Two backend deployment paths exist in this repo (`backend/` → Render,
`api/` → Vercel serverless). See `NEXT_STEPS.md` for why, and which one to
actually build on.

## Known gotchas

- `npm run lint` will show a large number of pre-existing `prettier/prettier`
  style findings (quote style, trailing commas) — real but low-priority
  cleanup debt, not a blocker.
- Generated files (`.vercel/output`, `backend/**/__pycache__`,
  `tsconfig.tsbuildinfo`) are gitignored — don't `git add -f` them back in.
