from app.services.scoring import build_default_components, compute_weighted_score


def test_compute_weighted_score_balanced() -> None:
    components = build_default_components(
        {
            "academic": 80,
            "technical": 90,
            "soft_skills": 75,
            "experience": 60,
            "integrations": 70,
        }
    )
    score = compute_weighted_score(components)
    assert isinstance(score, float)
    assert 0 <= score <= 100


def test_compute_weighted_score_empty_components() -> None:
    assert compute_weighted_score([]) == 0.0
