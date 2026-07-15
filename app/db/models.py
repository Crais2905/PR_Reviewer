import datetime
from typing import Optional, List

from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

from app.enums.review_status import ReviewStatus

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    firstname: Mapped[str] = mapped_column(String(256), nullable=False)
    lastname: Mapped[str] = mapped_column(String(256), nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=True)
    reviews: Mapped["Review"] = relationship("Review", back_populates="user", lazy="selectin")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    create_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.datetime.now)


class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    diff: Mapped[str] = mapped_column(Text, nullable=True)
    pr_url: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, default=ReviewStatus.pending.value)
    summary: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    overall_comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    risk: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    user: Mapped[User] = relationship("User", back_populates="reviews", lazy="selectin")
    problems: Mapped[List["ReviewProblems"]] = relationship("ReviewProblems", back_populates="review", lazy="selectin")
    create_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.datetime.now)


class ReviewProblems(Base):
    __tablename__ = "review_problems"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    review_id: Mapped[int] = mapped_column(Integer, ForeignKey("review.id"))
    review: Mapped[Review] = relationship("Review", back_populates="problems", lazy="selectin")
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    severity: Mapped[str] = mapped_column(String(512), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    recommendation: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(64), nullable=False)
