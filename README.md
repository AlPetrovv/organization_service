 # Organization Service

FastAPI service for managing organizations, buildings, and activities.

This service follows Domain-Driven Design (DDD) principles and Dependency Injection (DI) pattern.

## Key features

 - API key authentication via `X-API-Key` header (applies to all endpoints)
 - Async SQLAlchemy + Alembic migrations
 - Postgres + PostGIS support (GeoAlchemy2)
 - Versioned REST API under `/api/v1`

## Tech stack

 - Python 3.14
 - FastAPI + Uvicorn
 - SQLAlchemy (async) + Alembic
 - Dependency Injector
 - Postgres/PostGIS

## Configuration

The app is configured via environment variables using `pydantic-settings`.

Write your env files by templates

 ## API routes

Base prefix: `/api/v1`

 - `/activities`
 - `/orgs`
 - `/buildings`

Interactive API docs:

 - Swagger UI: `http://localhost:8000/docs`
 - ReDoc: `http://localhost:8000/redoc`
 - OpenAPI JSON: `http://localhost:8000/openapi.json`

## Authentication

All endpoints require the `X-API-Key` header.

Example:

```bash
curl -H 'X-API-Key: your-secret' http://localhost:8000/api/v1/orgs
```

 ## Run with Docker

 ```bash
 make build
 make run
 ```

Notes:

 - `make run` uses `docker compose up -d` and will start both the app and the database.
 - The container entrypoint runs migrations automatically on startup (`alembic upgrade head`).
 - The app is exposed on `http://localhost:8000`.


## Project structure (high level)

The main entrypoint is `app/src/main.py`.

 - `app/src/presentation/`
 - `app/src/application/`
 - `app/src/domain/`
 - `app/src/infra/`
 - `app/src/flows/`
