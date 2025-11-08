from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ScoreComponentBase(BaseModel):
    name: str
    weight: float = Field(ge=0)
    score: float = Field(ge=0, le=100)
    details: Optional[dict] = None


class ScoreComponentCreate(ScoreComponentBase):
    pass


class ScoreComponentOut(ScoreComponentBase):
    id: str

    class Config:
        from_attributes = True


class AssessmentBase(BaseModel):
    total_score: float
    insights: Optional[dict] = None


class AssessmentCreate(AssessmentBase):
    components: List[ScoreComponentCreate]


class AssessmentUpdate(AssessmentBase):
    pass


class AssessmentOut(AssessmentBase):
    id: str
    profile_id: str
    completion_time: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    components: List[ScoreComponentOut]

    class Config:
        from_attributes = True


class FeedbackEntry(BaseModel):
    id: str
    category: str
    message: str
    action_items: Optional[str] = None

    class Config:
        from_attributes = True


class AssessmentDetail(AssessmentOut):
    feedback_entries: List[FeedbackEntry]

    class Config:
        from_attributes = True


class AssessmentEvaluationRequest(BaseModel):
    academic: float = 0
    technical: float = 0
    soft_skills: float = 0
    experience: float = 0
    integrations: float = 0
    resume_html: Optional[str] = None
    github_username: Optional[str] = None
    linkedin_data: Optional[dict] = None
    cp_ratings: List[int] = []


class AssessmentEvaluationResponse(AssessmentDetail):
    resume_features: Optional[dict] = None
    github_summary: Optional[dict] = None
    linkedin_summary: Optional[dict] = None
    cp_summary: Optional[dict] = None
