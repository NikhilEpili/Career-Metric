from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from app.schemas.assessment import ScoreComponentCreate


@dataclass
class ScoringWeights:
    academic: float = 0.25
    technical: float = 0.35
    soft_skills: float = 0.2
    experience: float = 0.1
    integrations: float = 0.1


DEFAULT_WEIGHTS = ScoringWeights()


def compute_weighted_score(components: List[ScoreComponentCreate]) -> float:
    if not components:
        return 0.0

    weight_sum = sum(component.weight for component in components)
    if weight_sum <= 0:
        return 0.0

    cumulative = sum(component.score * component.weight for component in components)
    return round(cumulative / weight_sum, 2)


def build_default_components(raw_inputs: Dict[str, float]) -> List[ScoreComponentCreate]:
    mappings = {
        "academic": DEFAULT_WEIGHTS.academic,
        "technical": DEFAULT_WEIGHTS.technical,
        "soft_skills": DEFAULT_WEIGHTS.soft_skills,
        "experience": DEFAULT_WEIGHTS.experience,
        "integrations": DEFAULT_WEIGHTS.integrations,
    }

    components: List[ScoreComponentCreate] = []
    for name, weight in mappings.items():
        score = raw_inputs.get(name, 0.0)
        components.append(
            ScoreComponentCreate(
                name=name.replace("_", " ").title(),
                weight=weight,
                score=max(0.0, min(score, 100.0)),
                details={"raw": raw_inputs.get(name)},
            )
        )
    return components
