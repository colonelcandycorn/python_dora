from typing import List
from typing import Optional
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from enum import Enum

class Base(DeclarativeBase):
    pass

class Repository(Base):
    __tablename__ = 'repository'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    pull_requests: Mapped[List["PullRequest"]] = mapped_column(
        relationship("PullRequest", back_populates="repository")
    )
    commits: Mapped[List["Commit"]] = mapped_column(
        relationship("Commit", back_populates="repository")
    )

class Commit(Base):
    __tablename__ = 'commit'

    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column(String)
    author: Mapped[str] = mapped_column(String)
    repository_id: Mapped[int] = mapped_column(ForeignKey("repository.id"))
    repository: Mapped["Repository"] = mapped_column(
        relationship("Repository", back_populates="commits")
    )
    

class PullRequestState(Enum):
    OPEN = "open"
    CLOSED = "closed"
    MERGED = "merged"

class PullRequest(Base):
    __tablename__ = 'pull_request'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    body: Mapped[Optional[str]] = mapped_column(String)
    author: Mapped[str] = mapped_column(String)
    repository_id: Mapped[int] = mapped_column(ForeignKey("repository.id"))
    repository: Mapped["Repository"] = mapped_column(
        relationship("Repository", back_populates="pull_requests")
    )
    created_at: Mapped[DateTime] = mapped_column(DateTime)
    closed_at: Mapped[Optional[DateTime]] = mapped_column(DateTime)
    merged_at: Mapped[Optional[DateTime]] = mapped_column(DateTime)
    state: Mapped[PullRequestState]


