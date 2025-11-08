import { clsx } from "clsx";

interface StatusPillProps {
  status: "loading" | "online" | "offline";
  lastUpdated: Date | null;
}

const LABELS: Record<StatusPillProps["status"], string> = {
  loading: "Checking",
  online: "Live",
  offline: "Offline",
};

export function StatusPill({ status, lastUpdated }: StatusPillProps) {
  return (
    <span
      className={clsx("status-pill", {
        online: status === "online",
        offline: status === "offline",
        loading: status === "loading",
      })}
    >
      <span className="dot" />
      {LABELS[status]}
      {lastUpdated && status === "online" ? (
        <span className="timestamp">{lastUpdated.toLocaleTimeString()}</span>
      ) : null}
    </span>
  );
}
