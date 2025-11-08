from app.services.resume_parser import extract_resume_features


RESUME_HTML = """
<html>
<body>
  <p>Software Engineer with 3 years of experience in AI.</p>
  <ul>
    <li>Python</li>
    <li>FastAPI</li>
    <li>React</li>
  </ul>
  <a href="https://github.com/example">GitHub</a>
</body>
</html>
"""


def test_extract_resume_features() -> None:
    features = extract_resume_features(RESUME_HTML)
    assert features["links"], "Expected at least one hyperlink"
    assert features["keywords"], "Expected keyword extraction"
    assert features["word_count"] > 0
