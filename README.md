<<<<<<< HEAD
# production-monitoring
=======
# SmartLine Fullstack v4 (Monorepo)

This repo bundles the full stack:

- `frontend/` (Next.js App Router + Tailwind + Zustand hooks)
- `bff-service/` (Flask Backend-for-Frontend, HTTPS, cookie-based auth)
- `auth-service/` (Flask JWT + RBAC + Refresh + PostgreSQL + Alembic + seed)
- `file-export-service/` (Flask + Celery async export PDF/CSV/XLSX)
- `redis-service/` (Flask Redis Admin API + Redis server, JWT + RBAC)
- `docker-compose.yml` (one-command local run with HTTPS enabled on BFF)
- `.env` (environment variables override)

## Quick start (local)

```bash
# 1) Create RSA keys for RS256 (auth-service)
openssl genrsa -out private.pem 2048
openssl rsa -in private.pem -pubout -out public.pem

# 2) Copy into env (or export in shell)
cp .env.sample .env
# then edit .env to paste keys into JWT_PRIVATE_KEY_PEM and JWT_PUBLIC_KEY_PEM

# 3) Up the stack
docker compose up --build
```

- Frontend: http://localhost:3000
- BFF (HTTPS): https://localhost:8443
- Auth: http://localhost:5001
- Export: http://localhost:5002
- Redis Admin API: http://localhost:5003
- Redis TCP: localhost:6379
- Postgres: localhost:5432

## Vercel deployment (frontend)

- Set `NEXT_PUBLIC_BFF_BASE_URL` to your public BFF URL (e.g., `https://bff.yourdomain.com`)
- Do **not** point to `localhost` on Vercel.
- The `frontend/vercel.json` contains rewrites guidance if you prefer `/bff/*` in prod.

## Notes
- The BFF generates a self-signed certificate in-container for local HTTPS.
- All microservices validate RS256 JWTs via the `auth-service` JWKS endpoint.
>>>>>>> 438f9ec (initial commit with microservices and next frontend)
