import { useCallback, useEffect, useMemo, useState } from "react";

import { AuthPanel } from "./components/AuthPanel";
import { IntakeForm } from "./components/IntakeForm";
import { ScoreDashboard } from "./components/ScoreDashboard";
import { StatusPill } from "./components/StatusPill";
import { createProfile, evaluateAssessment, fetchHealth, getProfiles } from "./lib/api";
import type { Profile, ScoreSummary, UserSession } from "./lib/types";

const SESSION_STORAGE_KEY = "career-metric-session";

export function App() {
  const [healthStatus, setHealthStatus] = useState<"loading" | "online" | "offline">(
    "loading",
  );
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);
  const [session, setSession] = useState<UserSession | null>(null);
  const [profile, setProfile] = useState<Profile | null>(null);
  const [scoreData, setScoreData] = useState<ScoreSummary>({
    totalScore: 0,
    components: [],
    recommendations: [],
  });
  const [profileStatus, setProfileStatus] = useState<string | null>(null);

  useEffect(() => {
    async function checkHealth() {
      try {
        const data = await fetchHealth();
        if (data.status === "ok") {
          setHealthStatus("online");
          setLastUpdated(new Date());
        } else {
          setHealthStatus("offline");
        }
      } catch (error) {
        console.error(error);
        setHealthStatus("offline");
      }
    }

    checkHealth();
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  const bootstrapSession = useCallback(async (nextSession: UserSession) => {
    try {
      const profiles = await getProfiles(nextSession.token);
      let currentProfile = profiles[0];

      if (!currentProfile) {
        currentProfile = await createProfile(nextSession.token, {
          target_role: "Software Engineer",
          highest_education: "Bachelor",
          years_experience: 0,
        });
      }

      setSession(nextSession);
      setProfile(currentProfile);
      localStorage.setItem(SESSION_STORAGE_KEY, JSON.stringify(nextSession));
      setProfileStatus(
        `Ready to score for ${currentProfile.target_role ?? "your selected role"}.`,
      );
    } catch (error) {
      console.error(error);
      setProfileStatus("Unable to fetch profile. Please sign in again.");
      setSession(null);
      setProfile(null);
      localStorage.removeItem(SESSION_STORAGE_KEY);
    }
  }, []);

  useEffect(() => {
    const stored = localStorage.getItem(SESSION_STORAGE_KEY);
    if (stored) {
      try {
        const parsed: UserSession = JSON.parse(stored);
        bootstrapSession(parsed);
      } catch (error) {
        console.error("Failed to restore session", error);
        localStorage.removeItem(SESSION_STORAGE_KEY);
      }
    }
  }, [bootstrapSession]);

  const handleAuthenticated = useCallback(
    (nextSession: UserSession, nextProfile: Profile) => {
      setSession(nextSession);
      setProfile(nextProfile);
      localStorage.setItem(SESSION_STORAGE_KEY, JSON.stringify(nextSession));
      setProfileStatus(
        `Ready to score for ${nextProfile.target_role ?? "your selected role"}.`,
      );
    },
    [],
  );

  const handleLogout = useCallback(() => {
    setSession(null);
    setProfile(null);
    localStorage.removeItem(SESSION_STORAGE_KEY);
    setProfileStatus(null);
  }, []);

  const evaluate = useCallback(
    async (payload: Parameters<typeof evaluateAssessment>[2]) => {
      if (!session || !profile) {
        throw new Error("Authentication required");
      }
      return evaluateAssessment(profile.id, session.token, payload);
    },
    [profile, session],
  );

  const summary = useMemo(() => {
    return {
      strengths: scoreData.components.filter((item) => item.score >= 80),
      focus: scoreData.components.filter((item) => item.score < 60),
    };
  }, [scoreData]);

  return (
    <div className="app-shell">
      <header className="hero">
        <nav className="nav">
          <span className="brand">Career Metric</span>
          <div className="nav-right">
            <StatusPill status={healthStatus} lastUpdated={lastUpdated} />
            {session ? (
              <div className="nav-auth">
                <span className="muted">{session.email}</span>
                <button className="link-button" onClick={handleLogout}>
                  Sign out
                </button>
              </div>
            ) : null}
          </div>
        </nav>
        <div className="hero-content">
          <h1>AI-powered Employability Lens</h1>
          <p>
            Blend academic, technical, soft skill, and portfolio signals into a single
            actionable employability score. Pinpoint the next best move with tailored
            feedback and resources.
          </p>
        </div>
      </header>

      <main className="content">
        {session && profile ? (
          <section className="panel profile-card">
            <h2 className="panel-title">Welcome back, {profile.target_role ?? "talent"}</h2>
            <p className="panel-subtitle">
              {profileStatus ??
                "Your assessments will sync with the backend scoring engine automatically."}
            </p>
            <div className="profile-grid">
              <div>
                <span className="label">Primary role</span>
                <strong>{profile.target_role ?? "—"}</strong>
              </div>
              <div>
                <span className="label">Education</span>
                <strong>{profile.highest_education ?? "—"}</strong>
              </div>
              <div>
                <span className="label">Experience</span>
                <strong>{profile.years_experience ?? 0} yrs</strong>
              </div>
            </div>
          </section>
        ) : (
          <AuthPanel onAuthenticated={handleAuthenticated} />
        )}

        <section className="panel">
          <h2 className="panel-title">Tell us about your profile</h2>
          <p className="panel-subtitle">
            Upload your resume, share GitHub or LinkedIn highlights, and rate your comfort
            across skill areas to get an instant baseline.
          </p>
          <IntakeForm
            isAuthenticated={Boolean(session && profile)}
            onScoreGenerated={setScoreData}
            onEvaluate={session && profile ? evaluate : undefined}
          />
        </section>

        <section className="panel">
          <h2 className="panel-title">Personalised Readiness Overview</h2>
          <ScoreDashboard scoreData={scoreData} summary={summary} />
        </section>
      </main>
    </div>
  );
}
