import { ReactElement } from "react";
import { render, RenderOptions } from "@testing-library/react";

/**
 * Custom render function with providers
 * Use this instead of render from @testing-library/react
 */
export function renderWithProviders(
  ui: ReactElement,
  options?: Omit<RenderOptions, "wrapper">,
) {
  return render(ui, { ...options });
}

/**
 * Mock API response helper
 */
export function createMockResponse<T>(data: T, ok: boolean = true): Response {
  return {
    ok,
    json: async () => data,
    status: ok ? 200 : 400,
    statusText: ok ? "OK" : "Bad Request",
  } as Response;
}

