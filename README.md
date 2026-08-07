# cpoe-service

cpoe-service — domain: ehr

- **Port:** 8308
- **Language:** Python 3.11 + Flask
- **Database:** `ehr` (Postgres, table `cpoe`)
- **Event bus:** Kafka

## API

| Method    | Path                       |
|-----------|----------------------------|
| GET       | `/api/cpoe/`          |
| POST      | `/api/cpoe/`          |
| GET       | `/api/cpoe/<id>`      |
| PUT/PATCH | `/api/cpoe/<id>`      |
| DELETE    | `/api/cpoe/<id>`      |
| GET       | `/health`                  |
| GET       | `/ready`                   |

## Events

**Publishes:** order.placed
**Subscribes:** lab.result.available, imaging.result.available

## HTTP peer dependencies

- `ehr-service`
- `drug-interactions-service`
- `formulary-service`
- `audit-log-service`

## Local dev

```bash
pip install -e ../../libs/py-healthcare-common
pip install -r requirements.txt
cp .env.example .env
(cd ../../infra && docker compose up -d postgres kafka kafka-init)
python -m app.main
```

## Tests

```bash
pytest
```
