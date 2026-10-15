# WorkoutFlow API

WorkoutFlow API is a FastAPI application for tracking workouts and exercises. It uses AWS Cognito for authentication and PostgreSQL (SQLAlchemy 2.0 + Alembic) for storage. This guide covers running it locally with uvicorn.

## Contents

1. [Requirements](#requirements)
2. [Installation](#installation)
3. [AWS setup](#aws-setup)
4. [Configuration](#configuration)
5. [Database](#database)
6. [Running locally](#running-locally)
7. [Trying the API](#trying-the-api)
8. [Development](#development)
9. [API endpoints](#api-endpoints)
10. [Project layout](#project-layout)
11. [Troubleshooting](#troubleshooting)

## Requirements

- [uv](https://docs.astral.sh/uv/getting-started/installation/) 0.11 or newer. uv installs Python 3.14 (from `.python-version`) automatically.
- [Docker](https://docs.docker.com/get-docker/) for the local PostgreSQL (or any PostgreSQL 15+).
- [AWS CLI v2](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html), configured with credentials allowed to manage Cognito (only needed for the one-time AWS setup below).
- An AWS account.

## Installation

```sh
git clone https://github.com/gagatek1/WorkoutFlow-API.git
cd WorkoutFlow-API
uv sync
```

`uv sync` creates `.venv/` and installs runtime and development dependencies exactly as pinned in `uv.lock`.

## AWS setup

You need a Cognito user pool with an app client. Replace `eu-central-1` with your region.

```sh
export AWS_REGION=eu-central-1

POOL_ID=$(aws cognito-idp create-user-pool \
  --pool-name workoutflow \
  --username-attributes email \
  --auto-verified-attributes email \
  --query UserPool.Id --output text)

aws cognito-idp create-user-pool-client \
  --user-pool-id "$POOL_ID" \
  --client-name workoutflow-api \
  --generate-secret \
  --explicit-auth-flows ALLOW_USER_PASSWORD_AUTH ALLOW_REFRESH_TOKEN_AUTH \
  --query 'UserPoolClient.[ClientId,ClientSecret]' --output text

echo "$POOL_ID"
```

Note the pool id, client id and client secret for the configuration step. The client secret is optional: if you create the client without `--generate-secret`, leave `AWS_COGNITO_APP_CLIENT_SECRET` empty.

## Configuration

Copy the example file and fill in the values from the AWS setup:

```sh
cp .env.example .env
```

| Variable | Required | Description |
|---|---|---|
| `APP_STAGE` | no (`dev`) | `dev`, `test`, `staging` or `prod`. OpenAPI docs are disabled in `prod`. |
| `REGION_NAME` | yes | AWS region of Cognito, e.g. `eu-central-1`. |
| `DATABASE_URL` | yes | SQLAlchemy URL, e.g. `postgresql+psycopg://workoutflow:workoutflow@127.0.0.1:5432/workoutflow_db`. |
| `DATABASE_ECHO` | no (`false`) | Log SQL statements. Never in prod. |
| `DATABASE_POOL_SIZE` | no (`1`) | Connections per process (keep 1 behind Lambda, with RDS Proxy). |
| `AWS_COGNITO_APP_CLIENT_ID` | yes | App client id. |
| `AWS_COGNITO_APP_CLIENT_SECRET` | no | App client secret; empty for clients without a secret. |
| `AWS_COGNITO_USER_POOL_ID` | yes | User pool id. |

The app does not read AWS credentials from these variables. boto3 uses the standard AWS chain: `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY` (they can also go into `.env`) or `AWS_PROFILE`. Settings are validated at startup, so a missing or malformed value fails immediately with a clear error.

## Database

Start PostgreSQL and create the schema with Alembic:

```sh
docker compose up -d
uv run --env-file .env alembic upgrade head
```

The app never creates tables itself.

Existing v0.5 tables are not migrated: start from an empty database.

### Changing the schema

After changing a model, generate a migration and review it before committing:

```sh
uv run --env-file .env alembic revision --autogenerate -m "describe the change"
```

## Running locally

```sh
uv run --env-file .env uvicorn app.entrypoints.api.api_gateway_handler:app --reload
```

- API: http://127.0.0.1:8000/api/v1
- Health check: http://127.0.0.1:8000/api/v1/health
- Swagger UI: http://127.0.0.1:8000/api-docs (not available when `APP_STAGE=prod`)

On AWS Lambda the handler is `app.entrypoints.api.api_gateway_handler.lambda_handler` (v0.5 used `main.handler`).

## Trying the API

```sh
API=http://127.0.0.1:8000/api/v1

# 1. Sign up; Cognito emails a confirmation code and the API creates your profile
curl -s -X POST $API/auth/signup -H 'Content-Type: application/json' \
  -d '{"first_name": "Ada", "last_name": "Lovelace", "email": "you@example.com", "password": "Passw0rd!x"}'

# 2. Confirm the account with the code from the email
curl -s -X POST $API/auth/verify -H 'Content-Type: application/json' \
  -d '{"email": "you@example.com", "confirmation_code": "123456"}'

# 3. Sign in and keep the access token
TOKEN=$(curl -s -X POST $API/auth/signin -H 'Content-Type: application/json' \
  -d '{"email": "you@example.com", "password": "Passw0rd!x"}' \
  | python3 -c 'import json, sys; print(json.load(sys.stdin)["AccessToken"])')

# 4. Create a workout (date defaults to today) and add an exercise to it
WORKOUT_ID=$(curl -s -X POST $API/workouts -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"name": "Push day"}' | python3 -c 'import json, sys; print(json.load(sys.stdin)["id"])')

curl -s -X POST $API/workouts/$WORKOUT_ID/exercises -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"name": "Bench press", "sets": 3, "reps": 10, "weight": 60, "part": "chest"}'

# 5. See the workout total and list your workouts
curl -s "$API/workouts/$WORKOUT_ID" -H "Authorization: Bearer $TOKEN"
curl -s "$API/workouts?limit=20" -H "Authorization: Bearer $TOKEN"
```

Lists return `{"items": [...], "next_cursor": "..."}`. When `next_cursor` is not `null`, pass it back as `?cursor=` to get the next page.

## Development

All commands run inside the project's virtual environment through `uv run`.

| Task | Command |
|---|---|
| Install / update dependencies | `uv sync` |
| Add a runtime dependency | `uv add <package>` |
| Add a development dependency | `uv add --dev <package>` |
| Format code | `uv run ruff format .` |
| Lint (auto-fix safe issues with `--fix`) | `uv run ruff check .` |
| Type check | `uv run ty check --error-on-warning` |
| Check layer contracts | `uv run lint-imports` |
| Run all tests | `uv run pytest` |
| Run one test file | `uv run pytest tests/domain/workout/command_handlers/test_create_workout.py -x` |
| Coverage report | `uv run pytest --cov --cov-report=term-missing` |

GitHub Actions (`.github/workflows/ci.yml`) runs on every push to any branch and on pull requests, with two jobs: **lint** (formatting, ruff, ty, layer contracts, each as its own step) and **test** (pytest with coverage). To run the same checks locally before pushing:

```sh
uv run ruff format --check . && uv run ruff check . && uv run ty check --error-on-warning && uv run lint-imports && uv run pytest
```

Tests need no AWS account and no running database: by default the schema is created on in-memory SQLite (foreign keys enforced), Cognito is simulated with [moto](https://docs.getmoto.org/), rows are created with FactoryBoy factories (`tests/fixtures/factories.py`), and authentication is mocked with the `tokens` fixture.

SQLite ignores row locks, so the concurrency tests are skipped there. To run the whole suite against Postgres (CI does this in the `test-postgres` job), point `TEST_DATABASE_URL` at a throwaway database. The tests drop all tables, so never use your development database:

```sh
docker run -d --rm --name workoutflow-test-pg -e POSTGRES_USER=test -e POSTGRES_PASSWORD=test \
  -e POSTGRES_DB=workoutflow_test -p 55432:5432 postgres:17
TEST_DATABASE_URL=postgresql+psycopg://test:test@127.0.0.1:55432/workoutflow_test uv run pytest
docker stop workoutflow-test-pg
```

## API endpoints

All paths are under `/api/v1`. Every endpoint except the public ones requires `Authorization: Bearer <access token>`.

### Authentication

- **POST /auth/signup**: sign up and create the profile (public).
- **POST /auth/verify**: confirm the account with the emailed code (public).
- **POST /auth/signin**: sign in and get tokens (public).
- **POST /auth/token**: get a new access token from a refresh token (public).
- **POST /auth/change**: change the caller's password.
- **POST /auth/forgot**: send a password reset code (public).
- **POST /auth/confirm**: reset the password with the emailed code (public).
- **POST /auth/logout**: global sign-out, revokes every token of the caller.

### Profiles

- **GET /profiles/me**: get the caller's profile (names, total weight, workout count). Other users' profiles are not readable.
- **PUT /profiles/me**: create or update the caller's profile (names).

### Workouts

- **POST /workouts**: create a workout (`date` defaults to today in UTC; send it to use the client's local day).
- **GET /workouts**: list the caller's workouts (paginated).
- **GET /workouts/{workout_id}**: get one of the caller's workouts.
- **PUT /workouts/{workout_id}**: update a workout.
- **DELETE /workouts/{workout_id}**: delete a workout (it must have no exercises, otherwise 409).

### Exercises

- **POST /workouts/{workout_id}/exercises**: add an exercise; updates workout and profile totals.
- **GET /workouts/{workout_id}/exercises**: list the workout's exercises (paginated).
- **GET /workouts/{workout_id}/exercises/{exercise_id}**: get an exercise.
- **PUT /workouts/{workout_id}/exercises/{exercise_id}**: update an exercise; updates totals.
- **DELETE /workouts/{workout_id}/exercises/{exercise_id}**: delete an exercise; updates totals.

`part` is one of `back`, `biceps`, `chest`, `core`, `legs`, `shoulders`, `triceps`. Another user's workout or exercise answers 404.

### Users

- **PUT /users/me/email**: change the caller's email; Cognito sends a verification code to the new address.

## Project layout

```
app/
  settings.py                    typed configuration (pydantic-settings)
  domain/<context>/              identity, profile, workout, exercise
    commands/ command_handlers/  one write use case per file, one unit_of_work() transaction each
    entity.py                    SQLAlchemy model (entities/ when several)
    repository.py                XRepository(session): data access, never commits
    query_service.py             XQueryService class: reads
    schemas.py                   XRequest / XResponse pydantic models
    exceptions.py                business errors
  entrypoints/api/
    api_gateway_handler.py       FastAPI app, ROUTERS, error mapping, security headers
    v1/<resource>/<action>.py    one endpoint per file; __init__.py lists `routers`
  shared/
    auth/authorize.py            `with authorize_user(request.headers) as user:`
    clients/cognito.py           Cognito client
    db.py                        OrmBase, engine, unit_of_work()
    errors.py pagination.py types.py
migrations/                      Alembic environment and versions
tests/                           mirrors app/ (one test file and class per module); fixtures/ holds factories and mocks
```

Dependencies point one way only: entrypoints → domain → shared. `lint-imports` enforces this.

## Troubleshooting

- **`ValidationError` for `CognitoSettings` or `DatabaseSettings` at startup**: a required variable is missing or malformed in `.env` (see [Configuration](#configuration)).
- **`relation "user_profiles" does not exist`**: run `uv run --env-file .env alembic upgrade head`.
- **`NoCredentialsError` or `UnrecognizedClientException`**: boto3 found no valid AWS credentials. Set `AWS_PROFILE`, or put the keys in `.env` and start with `uv run --env-file .env ...`.
- **Creating a workout returns 404**: the caller has no profile (it is created at sign-up; if that failed, create it with `PUT /profiles/me`).
- **Sign-in returns 403 "Additional authentication step required"**: the pool asks for a new password or MFA, which this API does not support.
- **Sign-in returns 502**: Cognito failed, e.g. the app client does not allow `USER_PASSWORD_AUTH`.
- **Every call returns 401**: the access token expired (1 hour by default). Get a new one from `POST /auth/token` or sign in again.
