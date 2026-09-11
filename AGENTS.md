# Agent Rules for This Repo

This file exists because this project went through a real deployment mess: two
conflicting backends running simultaneously, a frontend silently pointed at the
wrong Vercel project, CORS blocking the actual live site, admin login and
table data missing entirely, and a menu category that only worked because of
mock data client-side. All of that is fixed now. Read this before touching
deployment config, env vars, seed scripts, or navigation/routing code.

## Exactly what is deployed, where

| Layer | Provider | Service/Project name | Live URL |
|---|---|---|---|
| Frontend | Vercel | `parivar-restaurant-final` | `https://parivar-restaurant-final.vercel.app` |
| Backend | Render | `parivar-backend` (web service) | `https://parivar-restaurant-final.onrender.com` |
| Database | Neon | project `dark-poetry-42301782` | direct (non-pooler) endpoint, `ap-southeast-2.aws.neon.tech` |

**Do not confuse these with similarly-named things that are NOT this project:**
- `parivar-rest.vercel.app` and `parivar.vercel.app` — neither belongs to this
  account. One is an unrelated static jQuery/Bootstrap template. Verified via
  direct inspection, not assumption — don't trust a plausible-looking URL
  without checking who owns it.
- `parivar-backend.onrender.com` — a completely different, unrelated Express
  app ("Parivar App Server is Running!", `x-powered-by: Express`). Not FastAPI,
  not this codebase, despite the name.
- `parivar-restaurant.com` / `www.parivar-restaurant.com` — DNS pointed at a
  **Weebly** site as of the last check, not Vercel. Re-verify before assuming
  this domain reaches the app described here.

The old Vercel-serverless backend path (`api/index.py`, SQLite copied to
`/tmp` on every cold start, data never persisted) has been **removed**. There
is exactly one backend now: FastAPI on Render, talking to Neon Postgres. If
you ever see `api/` reappear with a Python serverless function in it, or a
`rewrites` rule in `vercel.json` pointing `/api/*` somewhere, that's a
regression — stop and ask before "fixing" it either way.

## Rules

1. **Never commit or push without explicit, per-instance confirmation.** Not
   "the user said commit once earlier so it's fine now" — ask every time
   unless told otherwise for the rest of the session.

2. **Never assume a URL, project, or domain belongs to this app because the
   name looks right.** Verify live with `curl -i` (check response body and
   headers) before trusting it. This repo has three separate cases of a
   plausible URL belonging to someone/something else entirely.

3. **A `.env` file in the repo is not the source of truth for what's actually
   deployed.** Vite loads env files via `dotenv`, which does **not** override
   a value already set in `process.env` — so a dashboard-configured env var
   (Vercel, Render) silently wins over the committed file. When a deployed
   value looks wrong, check the platform dashboard's env vars first, not just
   the repo.

4. **`render.yaml` / `vercel.json` are specs, not guarantees.** If a service
   was created manually in a dashboard rather than via "New from Blueprint,"
   editing the YAML does **not** sync automatically — the dashboard's env vars
   have to be updated by hand too. Don't assume a config file push means the
   live service changed.

5. **Check where Render/Vercel actually look for config files.** Render reads
   `runtime.txt` from the **repo root**, not from `rootDir` when one is set —
   use the `PYTHON_VERSION` env var instead, it's rootDir-agnostic and
   reliable.

6. **Seed/migration scripts: check what "already seeded" actually checks.** A
   guard like "if any Category exists, skip everything" can silently prevent
   unrelated seeding (admin user, tables) from ever running once *any* other
   auto-seed has populated *anything*. Idempotency checks must be scoped to
   exactly what they're supposed to protect — not a proxy that happens to
   correlate most of the time.

7. **Don't seed placeholder/mock content into production without asking.**
   Generic seed data with broken image paths or filler descriptions looks
   worse than no data. If the frontend has fallback/mock data that duplicates
   what should be real backend data, ask which one is the source of truth
   before writing either into the database.

8. **CORS_ORIGINS must list the actual deployed frontend domain(s).** This
   broke once already (listed two domains that turned out not to be owned by
   this account, omitting the real one). Verify with an actual preflight
   request (`curl -X OPTIONS -H "Origin: <url>"`) against the live backend,
   not just by reading the config.

9. **FastAPI routes with a trailing slash will 307-redirect requests without
   one.** `curl` does not follow redirects by default (`-L` is required) and
   a plain `fetch()`/`axios` **does** follow them automatically — so a
   `curl` test without `-L` against `/api/v1/whatever` (no trailing slash)
   can show an empty/wrong result that isn't a real bug. Always test with `-L`
   or hit the exact path the router defines.

10. **Understand what a UI request actually means before changing routing.**
    "Clicking X should go to Y" is ambiguous between "navigate to a different
    route" and "scroll to a section on the current page." Confirm which one
    before touching `Link`/`href` targets — this repo had working
    scroll-to-section behavior nearly replaced with route navigation because
    of exactly this ambiguity.

11. **When something is reported broken in production, verify against the
    live deployment (`curl`, actual API responses), not just by reading
    source code.** Several bugs in this project's history existed only in
    what was *deployed*, not in what was in the repo at HEAD — reading code
    alone would have missed them.

12. **For major changes, confirm twice before acting** — see "Major changes"
    below.

## Coding standards & software principles

- **Match existing patterns.** Follow the conventions already in the codebase
  (module structure under `backend/app/modules/*`, naming, error handling,
  response shapes) rather than introducing a new style for new code.
- **Minimal, scoped changes.** Fix or build exactly what was asked. Don't
  refactor unrelated code, rename things "while you're in there," or bundle
  unrelated cleanup into a task-focused change.
- **No speculative abstractions.** Don't add config options, feature flags,
  or generic/reusable layers for needs that don't exist yet. Three similar
  lines beat a premature abstraction.
- **No unnecessary comments.** Code should read clearly from naming and
  structure. Only comment a genuinely non-obvious *why* (a workaround, a
  hidden constraint) — never restate *what* the code does.
- **Explicit over implicit.** Avoid silent fallbacks that mask a real problem
  — e.g. a `|| default` that quietly papers over a missing required config
  value in production instead of failing loudly. (See rule 6 above for how a
  too-broad idempotency guard did exactly this with seed data.)
- **Idempotent, re-runnable scripts by default** for anything that seeds or
  migrates data — assume it may run more than once against the same database.

## Security

- **Never hardcode secrets, API keys, or credentials** in source files. Use
  env vars, and never commit a `.env*` file containing real values (this repo
  already had `.env.production` tracked in git before being cleaned up).
- **Gate every mutating endpoint individually.** A `Depends(...)` auth check
  on a GET route does not imply POST/PUT/PATCH/DELETE on the same resource are
  protected — this codebase previously shipped unauthenticated writes on menu,
  category, and upload endpoints. Verify each one, don't infer from siblings.
- **Validate and sanitize input at the API boundary.** Don't trust
  client-supplied IDs, roles, prices, or amounts without server-side checks.
- **Default/seeded credentials are a standing risk, not a solved problem.**
  If you find or create default credentials (e.g. an `admin`/`admin123`
  seed), flag it clearly rather than silently rotating it yourself — that's
  the project owner's call, since changing it can lock them out.
- **CORS must allow only real, known origins** — never `"*"` in production.
  Verify with an actual preflight request against the live backend (rule 8).
- **Never log or print secrets** — full tokens, passwords, or connection
  strings — to console output, error messages, commit messages, or PR
  descriptions.

## Major changes: confirm twice

For anything with a wide blast radius — schema or migration changes, deleting
files or services, changes to auth/security logic, deployment config
(`render.yaml`, `vercel.json`, platform env vars), or anything touching
payments — confirm intent **twice**:

1. When the request comes in, restate what you understood and what you're
   about to do, before starting.
2. Immediately before executing the irreversible or high-impact step
   (running the migration, deleting the file, pushing the deploy config),
   summarize exactly what will change and get an explicit go-ahead — even if
   the user already said yes once earlier in the conversation. A single
   earlier "yes" does not cover a second, larger action later.
