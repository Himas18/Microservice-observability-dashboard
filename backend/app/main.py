import io
import csv
import psutil
from datetime import datetime
from typing import List
from fastapi import FastAPI, Depends, Query
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from . import models, schemas, crud
from .database import get_db, engine

app = FastAPI()

EXCLUDED_NAMES = {
    "system", "system idle process", "registry", "svchost.exe",
    "csrss.exe", "services.exe", "smss.exe", "wininit.exe", "conhost.exe"
}

startup_time = datetime.utcnow()

def scan_processes(db: Session):
    """
    Captures a snapshot of running processes and updates the DB.
    """
    fake_deps = {
        "python.exe": ["uvicorn.exe"],
        "streamlit.exe": ["python.exe"],
        "postgres.exe": ["pg_ctl.exe"]
    }
    for proc in psutil.process_iter(attrs=["name"]):
        try:
            name = proc.info["name"]
            dependencies = fake_deps.get(name.lower(), [])
            crud.create_or_update_service(db, schemas.ServiceStatus(
                name=name,
                status="up",
                dependencies=dependencies
            ))
        except Exception as e:
            print(f"[!] Failed to index '{proc.info.get('name')}' → {e}")

@app.on_event("startup")
def startup_sequence():
    """
    Initializes the database and captures an initial snapshot.
    """
    models.Base.metadata.create_all(bind=engine)
    print("🟢 Created services table")

    with Session(bind=engine.connect()) as db:
        scan_processes(db)

    print("📸 One-time process snapshot captured")

@app.on_event("shutdown")
def shutdown_sequence():
    """
    Drops the services table on app shutdown (ephemeral mode).
    """
    models.Base.metadata.drop_all(bind=engine, tables=[models.Service.__table__])
    print("🧹 Dropped services table on shutdown")

@app.post("/refresh")
def manual_refresh(db: Session = Depends(get_db)):
    """
    Triggers a new scan of system processes.
    """
    scan_processes(db)
    return {"message": "Services refreshed"}

@app.post("/status")
def receive_status(service: schemas.ServiceStatus, db: Session = Depends(get_db)):
    """
    Accepts service status from external scanner or clients.
    """
    return crud.create_or_update_service(db, service)

@app.get("/status", response_model=List[schemas.ServiceStatus])
def get_all_services(
    db: Session = Depends(get_db),
    exclude_common: bool = Query(True),
    name_filter: str = Query(None)
):
    """
    Retrieves all tracked services, with optional filters.
    """
    services = db.query(models.Service).all()

    if exclude_common:
        services = [s for s in services if s.name.lower() not in EXCLUDED_NAMES]

    if name_filter:
        services = [s for s in services if name_filter.lower() in s.name.lower()]

    return services

@app.get("/report")
def export_report(db: Session = Depends(get_db)):
    """
    Returns the full service report as JSON.
    """
    services = db.query(models.Service).all()
    report = [{
        "name": s.name,
        "status": s.status,
        "dependencies": s.dependencies,
        "last_updated": s.last_updated
    } for s in services]

    return JSONResponse(content=jsonable_encoder(report))

@app.get("/report_csv")
def download_csv(db: Session = Depends(get_db)):
    """
    Exports service data as downloadable CSV.
    """
    services = db.query(models.Service).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Name", "Status", "Dependencies", "Last Updated"])

    for s in services:
        writer.writerow([
            s.name,
            s.status,
            ", ".join(s.dependencies or []),
            s.last_updated
        ])

    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={
        "Content-Disposition": "attachment; filename=services_report.csv"
    })

@app.get("/health")
def health_check():
    """
    Health check endpoint with uptime.
    """
    uptime = (datetime.utcnow() - startup_time).total_seconds()
    return {"status": "ok", "uptime_seconds": uptime}