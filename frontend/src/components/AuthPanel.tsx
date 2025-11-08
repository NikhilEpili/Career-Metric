import { FormEvent, useState } from "react";

import { createProfile, getProfiles, login, register } from "../lib/api";
import type { Profile, UserSession } from "../lib/types";

interface AuthPanelProps {
  onAuthenticated: (session: UserSession, profile: Profile) => void;
}

export function AuthPanel({ onAuthenticated }: AuthPanelProps) {
  const [mode, setMode] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("candidate@example.com");
  const [password, setPassword] = useState("ChangeMe123!");
  const [fullName, setFullName] = useState("Candidate Persona");
  const [headline, setHeadline] = useState("Final-year engineering student | ML intern");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError(null);

    try {
      if (mode === "register") {
        await register({ email, password, full_name: fullName, headline });
      }

      const tokenResponse = await login(email, password);
      const session: UserSession = { token: tokenResponse.access_token, email };
      const profiles = await getProfiles(session.token);

      let profile = profiles[0];
      if (!profile) {
        profile = await createProfile(session.token, {
          target_role: "Software Engineer",
          highest_education: "Bachelor",
          years_experience: 0,
        });
      }

      onAuthenticated(session, profile);
    } catch (err) {
      console.error(err);
      setError(err instanceof Error ? err.message : "Unable to authenticate");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="panel auth-panel">
      <header className="auth-header">
        <h2>{mode === "login" ? "Sign in" : "Create an account"}</h2>
        <p>Authenticate to sync your assessments and unlock full analytics.</p>
      </header>

      <form onSubmit={handleSubmit} className="auth-form">
        <label>
          <span>Email address</span>
          <input
            type="email"
            autoComplete="email"
            required
            value={email}
            onChange={(event) => setEmail(event.target.value)}
          />
        </label>

        <label>
          <span>Password</span>
          <input
            type="password"
            autoComplete={mode === "login" ? "current-password" : "new-password"}
            required
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
        </label>

        {mode === "register" ? (
          <div className="register-grid">
            <label>
              <span>Full name</span>
              <input
                type="text"
                value={fullName}
                onChange={(event) => setFullName(event.target.value)}
              />
            </label>
            <label>
              <span>Headline</span>
              <input
                type="text"
                value={headline}
                onChange={(event) => setHeadline(event.target.value)}
              />
            </label>
          </div>
        ) : null}

        {error ? <p className="error-text">{error}</p> : null}

        <button className="cta" type="submit" disabled={loading}>
          {loading ? "Hold on..." : mode === "login" ? "Sign in" : "Register"}
        </button>
      </form>

      <footer className="auth-footer">
        <span>{mode === "login" ? "New here?" : "Already a member?"}</span>
        <button
          type="button"
          className="link-button"
          onClick={() => setMode(mode === "login" ? "register" : "login")}
        >
          {mode === "login" ? "Create an account" : "Use existing credentials"}
        </button>
      </footer>
    </div>
  );
}
