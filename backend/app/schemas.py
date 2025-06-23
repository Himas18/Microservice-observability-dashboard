from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class ServiceStatus(BaseModel):
    name: str
    status: str
    dependencies: Optional[List[str]] = []
    last_updated: Optional[datetime] = None

    class Config:
        orm_mode = True