from __future__ import annotations

from datetime import datetime

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.deps import get_current_user, get_db
from app.models.assessment import Assessment, ScoreComponent
from app.models.feedback import Feedback
from app.models.integration import IntegrationArtifact
from app.models.user import CandidateProfile, User
from app.schemas.assessment import (
    AssessmentEvaluationRequest,
    AssessmentEvaluationResponse,
)
from app.schemas.assessment import ScoreComponentOut
from app.services import (
    aggregate_cp_ratings,
    build_default_components,
    compute_weighted_score,
    enrich_linkedin_profile,
    extract_resume_features,
    fetch_github_profile,
    generate_feedback,
)

router = APIRouter()


async def _get_profile(session: AsyncSession, profile_id: str, user: User) -> CandidateProfile:
    profile = await session.get(CandidateProfile, profile_id)
    if not profile or profile.user_id != user.id:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.post(
    "/{profile_id}/evaluate",
    response_model=AssessmentEvaluationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def evaluate_profile(
    profile_id: str,
    payload: AssessmentEvaluationRequest,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AssessmentEvaluationResponse:
    profile = await _get_profile(session, profile_id, current_user)

    raw_inputs = {
        "academic": payload.academic,
        "technical": payload.technical,
        "soft_skills": payload.soft_skills,
        "experience": payload.experience,
        "integrations": payload.integrations,
    }
    component_payloads = build_default_components(raw_inputs)

    assessment = Assessment(
        profile_id=profile.id,
        total_score=compute_weighted_score(component_payloads),
        completion_time=datetime.utcnow(),
        insights={"inputs": raw_inputs},
    )

    for component_payload in component_payloads:
        assessment.components.append(
            ScoreComponent(
                name=component_payload.name,
                weight=component_payload.weight,
                score=component_payload.score,
                details=component_payload.details,
            )
        )

    session.add(assessment)
    await session.flush()

    component_schemas = [
        ScoreComponentOut.model_validate(component) for component in assessment.components
    ]

    feedback_suggestions = generate_feedback(component_schemas)
    for feedback_payload in feedback_suggestions:
        feedback = Feedback(assessment_id=assessment.id, **feedback_payload)
        session.add(feedback)

    resume_features = None
    github_summary = None
    linkedin_summary = None
    cp_summary = None

    if payload.resume_html:
        resume_features = extract_resume_features(payload.resume_html)
        session.add(
            IntegrationArtifact(
                profile_id=profile.id,
                source="resume",
                payload=resume_features,
            )
        )

    if payload.github_username:
        try:
            github_summary = await fetch_github_profile(payload.github_username)
            session.add(
                IntegrationArtifact(
                    profile_id=profile.id, source="github", payload=github_summary
                )
            )
        except httpx.HTTPError:
            github_summary = {"error": "Unable to fetch GitHub profile"}

    if payload.linkedin_data:
        linkedin_summary = enrich_linkedin_profile(payload.linkedin_data)
        session.add(
            IntegrationArtifact(
                profile_id=profile.id, source="linkedin", payload=linkedin_summary
            )
        )

    if payload.cp_ratings:
        cp_summary = aggregate_cp_ratings(payload.cp_ratings)
        session.add(
            IntegrationArtifact(
                profile_id=profile.id, source="cp", payload=cp_summary
            )
        )

    profile.current_score_id = assessment.id
    await session.commit()

    result = await session.execute(
        select(Assessment)
        .options(
            selectinload(Assessment.components),
            selectinload(Assessment.feedback_entries),
        )
        .where(Assessment.id == assessment.id)
    )
    persisted_assessment = result.scalar_one()

    response = AssessmentEvaluationResponse.model_validate(persisted_assessment)
    response.resume_features = resume_features
    response.github_summary = github_summary
    response.linkedin_summary = linkedin_summary
    response.cp_summary = cp_summary

    return response
