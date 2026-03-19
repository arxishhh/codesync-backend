from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class Document(BaseModel):
    uid : UUID
    title : str
    language : str
    content : bytes
    created_by : UUID
    created_at : datetime
    updated_at : datetime

class DocumentCreateModel(BaseModel):
    title : str
    language : str
    created_by : UUID



