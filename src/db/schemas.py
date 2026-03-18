from sqlmodel import SQLModel, Field, Column,Relationship
from sqlalchemy.dialects import postgresql as pg
from uuid import UUID, uuid4
from datetime import datetime
from typing import List

class User(SQLModel,table=True):

    __tablename__ = "users"

    uid : UUID = Field(sa_column=Column(pg.UUID(as_uuid=True),
                                        primary_key=True,
                                        nullable=False,
                                        default = uuid4()
                                        ))
    
    username : str = Field(sa_column=Column(pg.VARCHAR(10),
                                            nullable=False,
                                            unique=True))
    
    first_name : str
    last_name : str
    password_hash : str = Field(exclude =True)
    created_at : datetime = Field(sa_column=Column(pg.TIMESTAMP,
                                                   default=datetime.utcnow()))
    updated_at : datetime = Field(sa_column=Column(pg.TIMESTAMP,
                                                   default=datetime.utcnow()))
    
    documents : List["Document"] = Relationship(back_populates="users",
                                                sa_relationship_kwargs={'lazy':'selectin'})


class Document(SQLModel,table=True):
    __tablename__ = 'documents'

    uid : UUID = Field(
        sa_column=Column(pg.UUID(as_uuid=True),
                         primary_key=True,
                         nullable=False,
                         default=uuid4()))
    
    title : str = Field(
        sa_column=Column(pg.VARCHAR(10),
                         nullable=False,
                         default="Untitled")
    )
    content : bytes
    created_by : str = Field(
        sa_column = Column(pg.VARCHAR(),
                           nullable=False))
    
    created_at : datetime = Field(
        sa_column=Column(pg.TIMESTAMP,
                         default=datetime.utcnow()))
    
    updated_at : datetime = Field(
        sa_column=Column(pg.TIMESTAMP,
                         default=datetime.utcnow()))
    
    users : List["User"] = Relationship(back_populates="documents",sa_relationship_kwargs={'lazy':'selectin'})
    



