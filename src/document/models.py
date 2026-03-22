from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from enum import Enum

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

class Permission(str,Enum):
    EDIT = "edit"
    READ = "read"

class InviteModel(BaseModel):
    doc_id : str
    permission : Permission



