from __future__ import annotations

from typing import Any


def enrich_linkedin_profile(public_data: dict[str, Any]) -> dict[str, Any]:
    headline = public_data.get("headline", "")
    skills = public_data.get("skills", [])
    recommendations = public_data.get("recommendations", 0)

    return {
        "headline": headline,
        "skills": skills,
        "recommendations": recommendations,
        "skill_density": round(len(skills) / max(len(headline.split()), 1), 2)
        if headline
        else 0.0,
    }
