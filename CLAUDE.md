# CLAUDE.md — Guitar Instructor App

Operational guidance for Claude when working in this repository. Read
alongside `guitar-instructor-app-spec.md`, `guitar-instructor-app-project-plan.md`,
and `CONSTITUTION.md` — this file operationalizes the principles in the
constitution; it doesn't override them.

## Project Snapshot

Personal guitar practice app for an advanced player (30+ years), doubling as
a hands-on learning project for GitHub CI/CD, AWS, and Docker. Four modules,
**fixed build order**: Fretboard Literacy → Scale Fluency → Lick Library →
Picking Technique. Genre tagging (metal, jazz, country, extensible) cuts
across all four modules — it is not a separate module.

## Confirmed Stack — Don't Relitigate These

- **Frontend:** React + Tailwind, single responsive PWA (desktop/tablet/phone
  from one codebase, no native apps).
- **Visualization:** SVG components for fretboard diagrams; AlphaTab for tab
  notation and playback (confirmed via hands-on Playground review).
- **Backend:** FastAPI (Python) — chosen for the theory/math ecosystem and
  future audio-feature potential (pitch detection via librosa/aubio-style
  libraries).
- **Database:** one RDS Postgres instance (db.t4g.micro), three logical
  databases (`app_dev`, `app_qa`, `app_prod`) on it — not three instances, not
  Aurora Serverless.
- **Registry:** ECR.
- **Compute:** ECS Express Mode — dev/qa/prod services behind one shared ALB,
  Fargate-based, configured for Graviton/ARM64 to match native builds on the
  M5 MacBook Air. *(Superseded from an earlier App Runner plan: App Runner
  closed to new customers April 30, 2026. If you see App Runner referenced in
  older notes or memory, ECS Express Mode is the current decision.)*
- **IaC:** none. Console, CLI, or Express Mode's guided setup only — never
  propose Terraform or CDK.
- **CI/CD:** GitHub Actions. Build once → deploy-dev (auto) → deploy-qa
  (gated) → deploy-prod (gated), same artifact promoted throughout. Gates are
  GitHub Environments' required-reviewer rule on `qa` and `prod`.

## Content Rules — Hard Constraints

- Never scrape musical content from the web, and never let an LLM freehand
  notes/frets/tab from memory.
- **Canonical licks** (Module 3): hand-curated, one entry at a time.
- **Generated drills** (Modules 1, 2, 4): produced by a deterministic rules
  engine (scale formulas, interval math, genre presets) that Claude builds in
  code. An LLM may help pick creative parameters; the engine computes the
  actual notes/frets.
- If musical correctness is uncertain, flag it for Jeremy's review — don't
  guess and move on.

## Schema & Architecture Guardrails

- Exercise/lick schema stores structured reference data (target notes,
  timing, fret positions) from V1 — not just tab/rendering strings.
- Any metronome or timing code uses Web Audio API look-ahead scheduling, not
  `setInterval`/`setTimeout` naive timing.
- Exercise-generation logic lives behind a clean internal API boundary so
  future features (AI, audio analysis) can call in without a rewrite.

## Working Norms

- Task ownership follows the project plan's assignee column: **Jeremy** =
  accounts, credentials, provisioning, physical-device/musical verification.
  **Claude** = code, config, content drafts, CLI/console instructions. Don't
  attempt Jeremy's tasks (no credentials to do so anyway), and don't quietly
  skip Claude's.
- If a plan step depends on an external service that's changed or been
  deprecated, say so plainly rather than silently re-planning around it.
- Respect the fixed module build order — don't get ahead into Module 3/4
  before 1/2 have had their functional review.
- Before scaffolding or building, check this file plus the spec and plan
  docs. Don't reintroduce previously-rejected options: Terraform/CDK, Aurora
  Serverless, per-environment RDS instances, native mobile apps.

## Deferred — Not V1

"Play it for me" audio feedback, standalone metronome UI, "bet you can't play
this" challenge mode, and AI-driven song lookup against a personal
GP/MusicXML library are documented in the spec's Future Enhancements section
but not scheduled. Don't start building these unless Jeremy explicitly pulls
one forward — but do keep the Article V guardrails (structured schema,
accurate scheduling, clean API boundary) in mind for anything built now.
