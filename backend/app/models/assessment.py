from __future__ import annotations

from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.user import CandidateProfile
    from app.models.feedback import Feedback


class Assessment(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "assessments"

    profile_id: Mapped[str] = mapped_column(
        ForeignKey("candidate_profiles.id", ondelete="CASCADE"), index=True
    )
    total_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    completion_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    insights: Mapped[Optional[dict]] = mapped_column(JSON)

    profile: Mapped["CandidateProfile"] = relationship(back_populates="assessments")
    components: Mapped[List["ScoreComponent"]] = relationship(
        back_populates="assessment", cascade="all, delete-orphan"
    )
    feedback_entries: Mapped[List["Feedback"]] = relationship(
        back_populates="assessment", cascade="all, delete-orphan"
    )


class ScoreComponent(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "score_components"

    assessment_id: Mapped[str] = mapped_column(
        ForeignKey("assessments.id", ondelete="CASCADE"), index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    weight: Mapped[float] = mapped_column(Float, nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    details: Mapped[Optional[dict]] = mapped_column(JSON)

    assessment: Mapped["Assessment"] = relationship(back_populates="components")
