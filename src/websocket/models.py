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
    ERROR = "error"
    USER_JOINED = "user_joined"
    USER_LEFT = "user_left"
    CURSOR = "cursor"
    
class Message(BaseModel):
    message_type : Type
    payload : Optional[Dict[str,Any]] = None


class UserDetails(BaseModel):
    user_id : str
    username : str
    color : str
