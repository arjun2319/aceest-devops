# ACEest Fitness & Gym — DevOps CI/CD Pipeline

## About
Flask REST API for ACEest Fitness & Gym management system.
Built for BITS Pilani DevOps Assignment 2 (CSIZG514/SEZG514).

## Tech Stack
- Python 3.9 + Flask
- SQLite Database
- Docker + Kubernetes
- Jenkins CI/CD
- Pytest + SonarQube

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Health check |
| GET | /programs | List all programs |
| GET | /clients | List all clients |
| POST | /clients | Add new client |

## Run Locally
```bash
pip install -r requirements.txt
python app.py
