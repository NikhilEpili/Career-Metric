from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.user import CandidateProfile


class IntegrationArtifact(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "integration_artifacts"

    profile_id: Mapped[str] = mapped_column(
        ForeignKey("candidate_profiles.id", ondelete="CASCADE"), index=True
    )
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)

    profile: Mapped["CandidateProfile"] = relationship("CandidateProfile", backref="artifacts")
