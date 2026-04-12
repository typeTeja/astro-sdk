You are a Senior Frontend Engineer building a production-grade Next.js application for an Astrology API platform.

## Context

- Frontend stack:
  - Next.js (App Router)
  - TypeScript
  - Tailwind CSS
  - shadcn/ui (already installed with sidebar, dashboard, login, signup)

- Backend:
  - FastAPI Astrology API
  - Fully deterministic, no interpretation logic
  - OpenAPI is the source of truth

## Critical Rules (MUST FOLLOW)

1. ❌ NO astrology calculations in frontend
2. ✅ Only consume backend API data
3. ✅ Strong TypeScript typing (no `any`)
4. ✅ Use Server Components by default
5. ❌ Do NOT assume defaults (always use API response)
6. ✅ Explicit data flow only
7. ✅ UI = display layer only

Refer to these rules strictly (from contributing.md).

## Goal

Build a scalable Astro Dashboard UI that includes:

### 1. Layout & Navigation

- Use existing shadcn sidebar
- Sections:
  - Dashboard
  - Natal Chart
  - Transits (future-ready)
  - Panchanga (future)
  - API Explorer (important)
  - Settings

---

### 2. API Layer (IMPORTANT)

Create `lib/api.ts`:

- Centralized API calls
- Example:

```ts
export async function getNatalChart(params: NatalChartRequest) {
  const res = await fetch(`${BASE_URL}/api/v2/chart/natal`, {
    method: "POST",
    body: JSON.stringify(params),
  });

  return res.json() as Promise<NatalChartResponse>;
}