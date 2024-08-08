from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    trello_token: str


class Organization(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    trello_id: str = Field(unique=True)
    name: str
    is_selected: bool = Field(default=False)

    boards: List["Board"] = Relationship(back_populates="organization")


class Board(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    trello_id: str = Field(unique=True)
    name: str
    is_selected: bool = Field(default=False)
    organization_id: Optional[int] = Field(default=None, foreign_key="organization.id")

    organization: Optional[Organization] = Relationship(back_populates="boards")
    tasks: List["Task"] = Relationship(back_populates="board")


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    trello_id: str = Field(unique=True)
    name: str
    is_selected: bool = Field(default=False)
    hours_worked: int = Field(default=0)
    board_id: Optional[int] = Field(default=None, foreign_key="board.id")

    board: Optional[Board] = Relationship(back_populates="tasks")
