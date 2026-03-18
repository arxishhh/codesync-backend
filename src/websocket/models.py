from pydantic import BaseModel
from typing import Dict,Any
from enum import Enum
\

class Type(str,Enum):
    UPDATE = "update"
    JOIN = "join"
    AWARENESS = "awareness"
    LEAVE = "leave"
    


class Message(BaseModel):
    message_type : Type
    payload : Dict[str,Any]
