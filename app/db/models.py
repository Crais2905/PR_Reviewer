import datetime

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
    diff: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String, default=ReviewStatus.pending.value)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    user: Mapped[User] = relationship("User", back_populates="reviews", lazy="selectin")
    create_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.datetime.now)
