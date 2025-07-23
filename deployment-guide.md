
# Envacare Project Deployment Guide

This guide explains how to deploy both frontend and backend using Docker.

---

## Prerequisites

- Docker & Docker Compose installed
- `.env` files placed under `/backend` and `/frontend`

---

## Folder Structure

```
envacare-deploy/
├── backend/
│   ├── Dockerfile
│   ├── .env
│   └── [your backend source]
├── frontend/
│   ├── Dockerfile
│   ├── .env
│   └── [your frontend source]
├── docker-compose.yml
└── deployment-guide.md
```

---

## How to Run

```bash
# From root folder (envacare-deploy)
docker-compose up --build
```

- Backend runs on: http://localhost:8000
- Frontend runs on: http://localhost:3000

---

## Notes

- Update API URLs in `.env` files if needed.
- PostgreSQL DB is included in `docker-compose`.
- Make sure `requirements.txt` and `package.json` are valid.

---

## Troubleshooting

- Run `docker-compose down -v` to reset containers and volumes.
- Use `docker-compose logs` to view container logs.
