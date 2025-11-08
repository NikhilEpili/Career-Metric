import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { StatusPill } from "../StatusPill";

describe("StatusPill", () => {
  it("renders loading state", () => {
    render(<StatusPill status="loading" lastUpdated={null} />);
    expect(screen.getByText("Checking")).toBeInTheDocument();
  });

  it("renders online state", () => {
    const date = new Date();
    render(<StatusPill status="online" lastUpdated={date} />);
    expect(screen.getByText("Live")).toBeInTheDocument();
  });

  it("renders offline state", () => {
    render(<StatusPill status="offline" lastUpdated={null} />);
    expect(screen.getByText("Offline")).toBeInTheDocument();
  });
});

