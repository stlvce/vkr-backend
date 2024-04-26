from pydantic import BaseModel
from datetime import datetime


class DocumentOut(BaseModel):
    id: int
    title: str
    file_type: str
    link: str
    uploaded_at: datetime
