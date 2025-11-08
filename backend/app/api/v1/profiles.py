from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models.user import CandidateProfile, User
from app.schemas.user import (
    CandidateProfileCreate,
    CandidateProfileOut,
    CandidateProfileUpdate,
)

router = APIRouter()


@router.get("/", response_model=list[CandidateProfileOut])
async def list_profiles(
    session: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
) -> list[CandidateProfile]:
    result = await session.execute(
        select(CandidateProfile).where(CandidateProfile.user_id == current_user.id)
    )
    return result.scalars().all()


@router.post("/", response_model=CandidateProfileOut, status_code=status.HTTP_201_CREATED)
async def create_profile(
    payload: CandidateProfileCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CandidateProfile:
    profile = CandidateProfile(user_id=current_user.id, **payload.model_dump(exclude_unset=True))
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    return profile


@router.put("/{profile_id}", response_model=CandidateProfileOut)
async def update_profile(
    profile_id: str,
    payload: CandidateProfileUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CandidateProfile:
    profile = await session.get(CandidateProfile, profile_id)
    if not profile or profile.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Profile not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(profile, key, value)

    await session.commit()
    await session.refresh(profile)
    return profile


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(
    profile_id: str,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    profile = await session.get(CandidateProfile, profile_id)
    if not profile or profile.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Profile not found")

    await session.delete(profile)
    await session.commit()
