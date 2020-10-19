```bash
createdb sso

alembic revision -m "Create users and sessions table" --autogenerate
alembic upgrade head

python -m unittest v1.tests
```