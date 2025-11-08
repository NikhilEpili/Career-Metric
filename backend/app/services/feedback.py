from __future__ import annotations

from typing import Dict, List

from app.schemas.assessment import ScoreComponentOut


def generate_feedback(components: List[ScoreComponentOut]) -> List[Dict[str, str | None]]:
    entries: List[Dict[str, str | None]] = []
    for component in components:
        if component.score >= 80:
            message = f"Great job! Your {component.name} skills are a clear strength."
            action = "Continue refining your skills and mentor peers to reinforce your expertise."
        elif component.score >= 60:
            message = f"Solid {component.name} performance with room to grow."
            action = (
                "Identify one advanced project or certification to boost this area over the next month."
            )
        else:
            message = f"Focus on improving your {component.name.lower()} competencies."
            action = "Create a targeted improvement plan with measurable weekly goals."

        entries.append(
            {
                "category": component.name,
                "message": message,
                "action_items": action,
            }
        )
    return entries
