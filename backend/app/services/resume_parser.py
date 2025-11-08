from __future__ import annotations

from bs4 import BeautifulSoup


def extract_resume_features(resume_html: str) -> dict:
    soup = BeautifulSoup(resume_html, "html.parser")

    feature_summary = {
        "keywords": [tag.get_text(strip=True) for tag in soup.find_all("li")][:20],
        "paragraphs": len(soup.find_all("p")),
        "links": [a.get("href") for a in soup.find_all("a") if a.get("href")],
        "word_count": len(soup.get_text(separator=" ").split()),
    }
    feature_summary["keyword_density"] = round(
        feature_summary["word_count"] / max(feature_summary["paragraphs"], 1), 2
    )
    return feature_summary
