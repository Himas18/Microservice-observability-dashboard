## Microservice-observability-dashboard

A real-time system observability stack combining FastAPI, PostgreSQL, Streamlit, and a host-level scanner for process monitoring.

A full-stack system monitoring solution combining FastAPI, PostgreSQL, Streamlit, and a host-level scanner — all containerized with Docker Compose. Gain real-time insights into running processes, track API health, and visualize system activity from a clean dashboard.

## Tech Stack

- **Backend:** FastAPI + PostgreSQL
- **Frontend:** Streamlit dashboard
- **Scanner Service:** Host-level process monitor with `psutil`
- **Deployment:** Local docker compose 

## Features

- Real-time system process scanning
- REST API with health endpoints
- Streamlit dashboard with filters, color-coded statuses, and CSV export
- Dockerized services for local or cloud deployment
- Logs, timestamps, and service health tracking


## 🧪 Local Setup
Run the system either using Docker Compose (recommended) or directly on your machine using a virtual environment.

🐳 Option 1: Using Docker Compose (Recommended)

git clone https://github.com/Himas18/microservice-observability-dashboard.git
cd microservice-observability-dashboard
docker-compose up --build

This will spin up:
- FastAPI backend (on port 8000)
- Streamlit dashboard frontend (on port 8501)
- PostgreSQL database
Important: The scanner needs access to host-level system processes, so it runs outside the Docker environment.

In a new terminal, activate your environment and run:
python scanner/pc_scanner.py --loop --verbose

Access endpoints:
→ Backend API: http://localhost:8000/docs
→ Frontend dashboard: http://localhost:8501

💻 Option 2: Without Docker (Manual Setup)
Useful if you prefer local venv setup or want more granular control.

- Clone the repo and create a virtual environment:
  git clone https://github.com/Himas18/microservice-observability-dashboard.git
  cd microservice-observability-dashboard
  python -m venv venv
  venv\Scripts\activate   # On Windows
  source venv/bin/activate   # On macOS/Linux
- Install dependencies
  pip install -r backend/requirements.txt
  pip install -r frontend/requirements.txt
- Ensure PostgreSQL is running locally, and update connection strings if needed.
- Run the backend (FastAPI):
  cd backend
  uvicorn app.main:app --reload --port 8000
- Run the frontend (Streamlit):
  cd ../frontend
  streamlit run dashboard.py
- Run the scanner ( separate terminal ):
  python scanner/pc_scanner.py --loop --verbose


## 📂 Folder Structure
microservice-observability-dashboard/
├── backend/            # FastAPI app with models, CRUD, DB
├── frontend/           # Streamlit dashboard
├── scanner/            # Host-level process scanner
├── docker-compose.yml  # Docker multi-service orchestration
├── .gitignore
└── README.md

## Project status 
This project is in an actively developing state. Deployment to cloud platforms (e.g., Render, EC2) is planned for future stages.
