import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { IntakeForm } from "../IntakeForm";

describe("IntakeForm", () => {
  const mockOnScoreGenerated = vi.fn();
  const mockOnEvaluate = vi.fn();

  it("renders form inputs", () => {
    render(
      <IntakeForm
        isAuthenticated={false}
        onScoreGenerated={mockOnScoreGenerated}
      />,
    );

    expect(screen.getByLabelText(/academic index/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/technical depth/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/soft skills/i)).toBeInTheDocument();
  });

  it("updates score when form is submitted", async () => {
    render(
      <IntakeForm
        isAuthenticated={false}
        onScoreGenerated={mockOnScoreGenerated}
      />,
    );

    const submitButton = screen.getByRole("button", {
      name: /generate readiness score/i,
    });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockOnScoreGenerated).toHaveBeenCalled();
    });

    const callArgs = mockOnScoreGenerated.mock.calls[0][0];
    expect(callArgs).toHaveProperty("totalScore");
    expect(callArgs).toHaveProperty("components");
    expect(callArgs).toHaveProperty("recommendations");
  });

  it("calls onEvaluate when authenticated", async () => {
    const mockResponse = {
      id: "test-id",
      profile_id: "profile-id",
      total_score: 85,
      components: [
        { id: "1", name: "Academic", score: 80, weight: 0.25 },
      ],
      feedback_entries: [],
    };

    mockOnEvaluate.mockResolvedValue(mockResponse);

    render(
      <IntakeForm
        isAuthenticated={true}
        onScoreGenerated={mockOnScoreGenerated}
        onEvaluate={mockOnEvaluate}
      />,
    );

    const submitButton = screen.getByRole("button", {
      name: /generate readiness score/i,
    });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockOnEvaluate).toHaveBeenCalled();
    });
  });
});

