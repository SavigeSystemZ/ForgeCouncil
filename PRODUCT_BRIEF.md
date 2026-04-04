# Product Brief

Use this file to capture the product idea, intended user value, and chosen build shape for this repo.

## Product frame

- Product name: Forge Council
- Product category: set once the product shape is specific enough to exclude lookalikes
- One-line summary: define the app promise in one clear sentence before major implementation begins
- Why it should exist: capture the user pain, operator leverage, or market opportunity this app resolves
- Primary users: name the real people or operators who should benefit first
- Primary workflows: list the core flows the first milestone must prove
- Success indicators: record the measurable signal that shows the app is genuinely useful
- Non-goals: state what this repo should not try to solve in the first phase

## Experience bar

- Visual direction: deliberate, differentiated, and product-specific rather than template-generic
- Interaction bar: fast, clear, low-friction flows with designed states from the first milestone
- Performance bar: snappy enough that the first slice feels trustworthy under normal use
- Reliability bar: clear degraded states, explicit error handling, and no fake capability claims
- Trust and safety bar: security-conscious defaults, honest validation claims, and explicit handling of risky actions

## Build shape

- Recommended starter blueprint: manual review required
- Recommendation confidence: low
- Recommendation rationale: No single starter blueprint is dominant yet. Current signals are too weak or too generic. Refine PRODUCT_BRIEF.md or add real runtime signals, then review the recommendation again.
- Selected starter blueprint: not yet selected
- Why this blueprint fits: choose a starter blueprint after the product frame and delivery surfaces are clearer
- Planned repo shape: decide after selecting a starter blueprint
- First milestone: prove one end-to-end user-facing or operator-facing slice with real validation
- Initial validation focus: confirm one real build, launch, test, or smoke path early and keep it passing
- Next decision gates: starter blueprint, persistence model, deployment targets, packaging expectations, and AI scope

## Usage rules

- Keep this aligned with `_system/PROJECT_PROFILE.md`, `PLAN.md`, `ROADMAP.md`, `DESIGN_NOTES.md`, and `ARCHITECTURE_NOTES.md`.
- If the repo is greenfield, use `bootstrap/recommend-starter-blueprint.sh` first, then use `bootstrap/apply-starter-blueprint.sh` to stamp the explicitly chosen starter blueprint into the first operating surfaces.
- Keep this factual and product-specific; do not turn it into vague aspiration or marketing filler.
