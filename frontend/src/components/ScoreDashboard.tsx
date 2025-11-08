import { Chart as ChartJS, Filler, Legend, PointElement, RadialLinearScale, Tooltip } from "chart.js";
import { Radar } from "react-chartjs-2";

import type { ScoreSummary } from "../lib/types";

ChartJS.register(RadialLinearScale, PointElement, Filler, Tooltip, Legend);

interface ScoreDashboardProps {
  scoreData: ScoreSummary;
  summary: {
    strengths: Array<{ name: string; score: number }>;
    focus: Array<{ name: string; score: number }>;
  };
}

export function ScoreDashboard({ scoreData, summary }: ScoreDashboardProps) {
  const hasData = scoreData.components.length > 0;

  const radarData = hasData
    ? {
        labels: scoreData.components.map((item) => item.name),
        datasets: [
          {
            label: "Score",
            data: scoreData.components.map((item) => item.score),
            backgroundColor: "rgba(99, 102, 241, 0.2)",
            borderColor: "rgba(99, 102, 241, 1)",
            borderWidth: 2,
            pointBackgroundColor: "rgba(99, 102, 241, 1)",
          },
        ],
      }
    : {
        labels: ["Academic", "Technical", "Soft Skills", "Experience", "Portfolio"],
        datasets: [
          {
            label: "Score",
            data: [40, 40, 40, 40, 40],
            backgroundColor: "rgba(99, 102, 241, 0.05)",
            borderColor: "rgba(99, 102, 241, 0.2)",
            borderWidth: 1,
            pointBackgroundColor: "rgba(99, 102, 241, 0.2)",
          },
        ],
      };

  const radarOptions = {
    scales: {
      r: {
        beginAtZero: true,
        angleLines: { color: "rgba(255,255,255,0.1)" },
        grid: { color: "rgba(255,255,255,0.1)" },
        ticks: { showLabelBackdrop: false, color: "#94a3b8" },
        suggestedMax: 100,
      },
    },
    plugins: {
      legend: { display: false },
    },
    responsive: true,
    maintainAspectRatio: false,
  } as const;

  return (
    <div className="dashboard-grid">
      <div className="overview">
        <span className="label">Readiness score</span>
        <h3>{scoreData.totalScore}</h3>
        <p>
          Weighted aggregate of your academic profile, technical depth, behavioural finesse,
          experience, and portfolio signals.
        </p>
      </div>

      <div className="chart-card">
        {hasData ? (
          <Radar data={radarData} options={radarOptions} />
        ) : (
          <div className="chart-placeholder">
            Provide inputs to visualise your readiness radar.
          </div>
        )}
      </div>

      <div className="components">
        {hasData ? (
          scoreData.components.map((component) => (
            <div key={component.name} className="component-card">
              <header>
                <span>{component.name}</span>
                <strong>{component.score}</strong>
              </header>
              <div className="progress">
                <div
                  className="bar"
                  style={{ width: `${Math.min(component.score, 100)}%` }}
                />
              </div>
              <small>
                Weight: {component.weight ? (component.weight * 100).toFixed(0) : "n/a"}%
              </small>
            </div>
          ))
        ) : (
          <p className="muted">Your component breakdown will appear after scoring.</p>
        )}
      </div>

      <div className="recommendations">
        <h4>Next best actions</h4>
        {scoreData.recommendations.length ? (
          <ul>
            {scoreData.recommendations.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        ) : (
          <p className="muted">Submit your profile to unlock targeted guidance.</p>
        )}
      </div>

      <div className="summary">
        <div>
          <h5>Strengths</h5>
          <ul>
            {summary.strengths.length ? (
              summary.strengths.map((item) => <li key={item.name}>{item.name}</li>)
            ) : (
              <li>We will fill this as you submit!</li>
            )}
          </ul>
        </div>
        <div>
          <h5>Focus areas</h5>
          <ul>
            {summary.focus.length ? (
              summary.focus.map((item) => <li key={item.name}>{item.name}</li>)
            ) : (
              <li>Everything looks balanced so far.</li>
            )}
          </ul>
        </div>
      </div>

      {(scoreData.resume_features || scoreData.github_summary || scoreData.linkedin_summary || scoreData.cp_summary) && (
        <div className="integration-summary">
          <h4>Integrated Signals</h4>
          <div className="integration-grid">
            {scoreData.resume_features ? (
              <section>
                <h5>Resume</h5>
                <pre>{JSON.stringify(scoreData.resume_features, null, 2)}</pre>
              </section>
            ) : null}
            {scoreData.github_summary ? (
              <section>
                <h5>GitHub</h5>
                <pre>{JSON.stringify(scoreData.github_summary, null, 2)}</pre>
              </section>
            ) : null}
            {scoreData.linkedin_summary ? (
              <section>
                <h5>LinkedIn</h5>
                <pre>{JSON.stringify(scoreData.linkedin_summary, null, 2)}</pre>
              </section>
            ) : null}
            {scoreData.cp_summary ? (
              <section>
                <h5>Competitive Programming</h5>
                <pre>{JSON.stringify(scoreData.cp_summary, null, 2)}</pre>
              </section>
            ) : null}
          </div>
        </div>
      )}
    </div>
  );
}
