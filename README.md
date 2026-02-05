 # Organization Service
 
FastAPI service for managing organizations, buildings, and activities. 

This service follows Domain-Driven Design (DDD) principles and Dependency Injection (DI) pattern.

 ## Tech stack

 - Python 3.14
 - FastAPI + Uvicorn
 - SQLAlchemy (async) + Alembic
 - Dependency Injector
 - Postgres/PostGIS

 ## API routes

 Base prefix: `/api/v1`

 - `/activities`
 - `/orgs`
 - `/buildings`

 ## Run with Docker (dev)

 ```bash
 make build
 make run
 ```

 ## Database migrations

 From the `app/` directory:

 ```bash
 poetry run alembic upgrade head
 ```
