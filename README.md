## Microservice-observability-dashboard

A real-time observability system combining FastAPI, PostgreSQL, Streamlit, and a host-level scanner — all orchestrated with Docker Compose. Gain live insights into running system processes, monitor API uptime, and visualize operational health through a clean and responsive dashboard.

## Tech Stack

- **Backend:** FastAPI + PostgreSQL
- **Frontend:** Streamlit dashboard
- **Scanner Service:** Host-level process monitor with `psutil`,`psutil`,`pyyaml`
- **Deployment:** Local docker compose(Render ready)

## Features

- Real-time system process scanning
- REST API with health endpoints
- Streamlit dashboard with filters, color-coded statuses, and CSV export
- Timestamps, logs, and health tracking baked into each service
- Modular architecture ready for local or future cloud deployment



## 🧪 Local Setup
Run the system either using Docker Compose (recommended) or directly on your machine using a virtual environment.

🐳 Option 1: Using Docker Compose (Recommended)

git clone https://github.com/Himas18/microservice-observability-dashboard.git
cd microservice-observability-dashboard
docker-compose up --build

This will spin up:
- FastAPI backend at http://localhost:8000/docs
- Streamlit dashboard at http://localhost:8501
- PostgreSQL database
Important: The scanner service runs on your local machine to access OS-level process data.

In a separate terminal :
python -m venv venv
venv\Scripts\activate         # Windows
source venv/bin/activate      # macOS/Linux
pip install -r scanner/requirements.txt
python scanner/pc_scanner.py --loop --verbose

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
  pip install -r scanner/requirements.txt

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
├── backend/            # FastAPI app with DB model and routes
├── frontend/           # Streamlit dashboard logic
├── scanner/            # Host-level process scanner with psutil & requests
├── docker-compose.yml  # Docker multi-service orchestration
├── .gitignore
└── README.md

## Project status 
This project is in an actively developing state. Deployment to cloud platforms (e.g., Render, EC2) is planned for future stages.
