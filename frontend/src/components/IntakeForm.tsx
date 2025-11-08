import { FormEvent, useMemo, useState } from "react";

import type {
  AssessmentEvaluationRequest,
  AssessmentEvaluationResponse,
  ScoreSummary,
} from "../lib/types";

interface IntakeFormProps {
  isAuthenticated: boolean;
  onScoreGenerated: (payload: ScoreSummary) => void;
  onEvaluate?: (
    payload: AssessmentEvaluationRequest,
  ) => Promise<AssessmentEvaluationResponse>;
}

export function IntakeForm({ isAuthenticated, onScoreGenerated, onEvaluate }: IntakeFormProps) {
  const [academic, setAcademic] = useState(75);
  const [technical, setTechnical] = useState(80);
  const [softSkills, setSoftSkills] = useState(70);
  const [experience, setExperience] = useState(3);
  const [github, setGithub] = useState("octocat");
  const [linkedinHeadline, setLinkedinHeadline] = useState(
    "Aspiring SDE | Hackathon finalist",
  );
  const [cpRatings, setCpRatings] = useState("1800, 1900, 2050");
  const [resumeName, setResumeName] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [status, setStatus] = useState<string | null>(null);

  const softRecommendations = useMemo(() => {
    const suggestions = [] as string[];
    if (technical < 70) {
      suggestions.push(
        "Join a weekend hackathon or ship a micro-saas to sharpen technical delivery.",
      );
    }
    if (academic < 65) {
      suggestions.push("Revisit core CS concepts—algorithms, data structures, and DBMS.");
    }
    if (softSkills < 60) {
      suggestions.push("Practice behavioural interviews with STAR stories for key roles.");
    }
    if (experience < 2) {
      suggestions.push(
        "Add capstone projects or freelance gigs to demonstrate applied experience.",
      );
    }
    if (!suggestions.length) {
      suggestions.push("Great baseline! Double down on advanced certifications this month.");
    }
    return suggestions;
  }, [technical, academic, softSkills, experience]);

  function handleResumeUpload(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    setResumeName(file ? file.name : null);
  }

  function buildLocalSummary(): ScoreSummary {
    const weights = {
      academic: 0.25,
      technical: 0.35,
      softSkills: 0.2,
      experience: 0.1,
      integrations: 0.1,
    } as const;

    const computedIntegrations = [github, linkedinHeadline, resumeName]
      .filter(Boolean)
      .length
      ? 90
      : 60;

    const components = [
      { name: "Academic", score: academic, weight: weights.academic },
      { name: "Technical", score: technical, weight: weights.technical },
      { name: "Soft Skills", score: softSkills, weight: weights.softSkills },
      {
        name: "Experience",
        score: Math.min(100, experience * 10 + 30),
        weight: weights.experience,
      },
      {
        name: "Portfolio",
        score: computedIntegrations,
        weight: weights.integrations,
      },
    ];

    const weightSum = Object.values(weights).reduce((acc, weight) => acc + weight, 0);
    const weightedTotal =
      components.reduce((acc, item) => acc + item.score * item.weight, 0) / weightSum;

    return {
      totalScore: Math.round(weightedTotal),
      components,
      recommendations: softRecommendations,
    };
  }

  function parseRatings(): number[] {
    return cpRatings
      .split(",")
      .map((rating) => Number(rating.trim()))
      .filter((value) => !Number.isNaN(value) && value > 0);
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setStatus(null);

    const localSummary = buildLocalSummary();

    if (isAuthenticated && onEvaluate) {
      const payload: AssessmentEvaluationRequest = {
        academic,
        technical,
        soft_skills: softSkills,
        experience: Math.min(100, experience * 10 + 30),
        integrations: localSummary.components.find((item) => item.name === "Portfolio")?.score ?? 70,
        resume_html: resumeName ? `<p>Resume uploaded: ${resumeName}</p>` : undefined,
        github_username: github || undefined,
        linkedin_data: linkedinHeadline
          ? {
              headline: linkedinHeadline,
              skills: linkedinHeadline.split(" ").slice(0, 10),
            }
          : undefined,
        cp_ratings: parseRatings(),
      };

      try {
        const response = await onEvaluate(payload);
        const summary: ScoreSummary = {
          totalScore: Math.round(response.total_score),
          components: response.components,
          recommendations: response.feedback_entries.map((item) =>
            item.action_items
              ? `${item.message} — ${item.action_items}`
              : item.message,
          ),
          resume_features: response.resume_features ?? undefined,
          github_summary: response.github_summary ?? undefined,
          linkedin_summary: response.linkedin_summary ?? undefined,
          cp_summary: response.cp_summary ?? undefined,
        };
        onScoreGenerated(summary);
        setStatus("Synced with backend scoring engine.");
        setSubmitting(false);
        return;
      } catch (error) {
        console.error(error);
        setStatus("Falling back to local estimation (API unavailable).");
      }
    }

    onScoreGenerated(localSummary);
    setStatus("Local estimation generated. Sign in to sync with backend.");
    setSubmitting(false);
  }

  return (
    <form className="intake-form" onSubmit={handleSubmit}>
      <div className="form-grid">
        <label>
          <span>Academic index</span>
          <input
            type="range"
            min={30}
            max={100}
            step={1}
            value={academic}
            onChange={(event) => setAcademic(Number(event.target.value))}
          />
          <strong>{academic}</strong>
        </label>

        <label>
          <span>Technical depth</span>
          <input
            type="range"
            min={30}
            max={100}
            value={technical}
            onChange={(event) => setTechnical(Number(event.target.value))}
          />
          <strong>{technical}</strong>
        </label>

        <label>
          <span>Soft skills</span>
          <input
            type="range"
            min={30}
            max={100}
            value={softSkills}
            onChange={(event) => setSoftSkills(Number(event.target.value))}
          />
          <strong>{softSkills}</strong>
        </label>

        <label>
          <span>Industry experience (years)</span>
          <input
            type="number"
            min={0}
            max={20}
            value={experience}
            onChange={(event) => setExperience(Number(event.target.value))}
          />
        </label>

        <label>
          <span>GitHub username</span>
          <input
            type="text"
            placeholder="octocat"
            value={github}
            onChange={(event) => setGithub(event.target.value)}
          />
        </label>

        <label>
          <span>LinkedIn headline</span>
          <input
            type="text"
            placeholder="Aspiring Data Scientist @ Campus AI"
            value={linkedinHeadline}
            onChange={(event) => setLinkedinHeadline(event.target.value)}
          />
        </label>

        <label>
          <span>CP ratings (comma-separated)</span>
          <input
            type="text"
            placeholder="1800, 1900, 2050"
            value={cpRatings}
            onChange={(event) => setCpRatings(event.target.value)}
          />
        </label>

        <label className="file-upload">
          <span>Resume (PDF/DOCX)</span>
          <input type="file" accept=".pdf,.doc,.docx" onChange={handleResumeUpload} />
          {resumeName ? <em>{resumeName}</em> : <em>No file selected</em>}
        </label>
      </div>

      <div className="form-actions">
        <button className="cta" type="submit" disabled={submitting}>
          {submitting ? "Scoring..." : "Generate readiness score"}
        </button>
        {status ? <span className="status-hint">{status}</span> : null}
      </div>
    </form>
  );
}
