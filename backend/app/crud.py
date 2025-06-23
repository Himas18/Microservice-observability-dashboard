from sqlalchemy.orm import Session
from datetime import datetime
from . import models, schemas

def create_or_update_service(db: Session, service: schemas.ServiceStatus) -> models.Service:
    """
    Creates a new service record or updates an existing one based on service name.
    """
    existing = db.query(models.Service).filter_by(name=service.name).first()

    if existing:
        existing.status = service.status
        existing.dependencies = service.dependencies or []
        existing.last_updated = datetime.utcnow()
    else:
        existing = models.Service(
            name=service.name,
            status=service.status,
            dependencies=service.dependencies or [],
            last_updated=datetime.utcnow()
        )
        db.add(existing)

    db.commit()
    db.refresh(existing)
    return existing