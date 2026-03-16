from pydantic import BaseModel
from typing import Dict,Any

class Message(BaseModel):
    type : str
    payload : Dict[str,Any]
