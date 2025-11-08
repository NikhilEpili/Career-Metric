"""Initial database schema"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "20241107_01_init"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=True),
        sa.Column("headline", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column(
            "is_superuser", sa.Boolean(), nullable=False, server_default=sa.text("false")
        ),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=False)

    op.create_table(
        "candidate_profiles",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("target_role", sa.String(length=255), nullable=True),
        sa.Column("highest_education", sa.String(length=255), nullable=True),
        sa.Column("years_experience", sa.Float(), nullable=True),
        sa.Column("current_score_id", sa.String(length=36), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    )

    op.create_table(
        "assessments",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("profile_id", sa.String(length=36), nullable=False),
        sa.Column("total_score", sa.Float(), nullable=False, server_default="0"),
        sa.Column("completion_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("insights", sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(["profile_id"], ["candidate_profiles.id"], ondelete="CASCADE"),
    )
    op.create_index(
        op.f("ix_assessments_profile_id"), "assessments", ["profile_id"], unique=False
    )

    op.create_table(
        "integration_artifacts",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("profile_id", sa.String(length=36), nullable=False),
        sa.Column("source", sa.String(length=100), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(["profile_id"], ["candidate_profiles.id"], ondelete="CASCADE"),
    )
    op.create_index(
        op.f("ix_integration_artifacts_profile_id"),
        "integration_artifacts",
        ["profile_id"],
        unique=False,
    )

    op.create_table(
        "score_components",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("assessment_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("weight", sa.Float(), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("details", sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(["assessment_id"], ["assessments.id"], ondelete="CASCADE"),
    )
    op.create_index(
        op.f("ix_score_components_assessment_id"),
        "score_components",
        ["assessment_id"],
        unique=False,
    )

    op.create_table(
        "feedback_entries",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("assessment_id", sa.String(length=36), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("action_items", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["assessment_id"], ["assessments.id"], ondelete="CASCADE"),
    )
    op.create_index(
        op.f("ix_feedback_entries_assessment_id"),
        "feedback_entries",
        ["assessment_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_feedback_entries_assessment_id"), table_name="feedback_entries")
    op.drop_table("feedback_entries")
    op.drop_index(op.f("ix_score_components_assessment_id"), table_name="score_components")
    op.drop_table("score_components")
    op.drop_index(
        op.f("ix_integration_artifacts_profile_id"), table_name="integration_artifacts"
    )
    op.drop_table("integration_artifacts")
    op.drop_index(op.f("ix_assessments_profile_id"), table_name="assessments")
    op.drop_table("assessments")
    op.drop_table("candidate_profiles")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
