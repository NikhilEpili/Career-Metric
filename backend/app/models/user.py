from __future__ import annotations

from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.assessment import Assessment


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(255))
    headline: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    profiles: Mapped[List["CandidateProfile"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class CandidateProfile(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "candidate_profiles"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    target_role: Mapped[Optional[str]] = mapped_column(String(255))
    highest_education: Mapped[Optional[str]] = mapped_column(String(255))
    years_experience: Mapped[Optional[float]] = mapped_column(Float, default=0.0)
    current_score_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)

    user: Mapped["User"] = relationship(back_populates="profiles")
    assessments: Mapped[List["Assessment"]] = relationship(
        back_populates="profile", cascade="all, delete-orphan"
    )
