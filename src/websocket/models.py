from pydantic import BaseModel
from typing import Dict,Any,Optional
from enum import Enum
\

class Type(str,Enum):
    UPDATE = "update"
    JOIN = "join"
    AWARENESS = "awareness"
    LEAVE = "leave"
    SYNC = "sync"
    


class Message(BaseModel):
    message_type : Type
    payload : Optional[Dict[str,Any]] = None
