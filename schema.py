from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TaskSchema(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    is_complete: Optional[bool] = False

    