from datetime import datetime

from pydantic import BaseModel


class IntegrationArtifactBase(BaseModel):
    source: str
    payload: dict


class IntegrationArtifactCreate(IntegrationArtifactBase):
    pass


class IntegrationArtifactOut(IntegrationArtifactBase):
    id: str
    profile_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
