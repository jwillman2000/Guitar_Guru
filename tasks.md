# Tasks

Running log of what's done and what's left, so we don't lose our place
between sporadic sessions. Mirrors the phases in
`guitar-instructor-app-project-plan.md` — see that file for full task
notes; this one is just status tracking.

Last updated: 2026-08-31

## Status at a glance

- **Phases 0–4 are complete.** All four core modules built, reviewed, and
  merged (PRs #1–10). Visualization (SVG fretboard + AlphaTab) is done.
- **Working locally only right now.** Jeremy has unspecified items he wants
  to address before this goes to AWS — Phase 7 (and anything that assumes
  AWS is live) is on hold until he says otherwise. Don't start Phase 7 work
  unprompted.
- **Next up:** Phase 5 (Responsive/PWA) and/or Phase 6 (Containerization) —
  both local-only, no AWS needed. Order is Jeremy's call.

## Phase 0 — Accounts & Local Environment

- [x] AWS account, IAM admin user + MFA, GitHub repo, Docker Desktop,
      Node.js — all done (project has been building/pushing PRs throughout)
- [ ] Confirm ECS Express Mode task uses Graviton (ARM64) — deferred
      alongside Phase 7, since there's no ECS resource yet to configure

## Phase 1 — Repo & Project Scaffold ✅ done

- [x] React + Tailwind frontend scaffold
- [x] FastAPI backend scaffold
- [x] Initial Dockerfile(s)
- [x] Pushed to GitHub, branch protection on `main`

## Phase 2 — Data Layer ✅ done

- [x] Postgres schema (exercises, licks, tags)
- [x] Alembic migrations
- [x] Tag taxonomy seed script (genre/technique/position)
- [x] RDS Postgres instance (`guitar-guru-db`, db.t4g.micro)
- [x] `app_dev` / `app_qa` / `app_prod` databases
- [x] Migrations/seed run against RDS

## Phase 3 — Core Modules ✅ done

- [x] Module 1 — Fretboard note-mapping engine
- [x] Module 2 — Scale fluency generator (3nps + pentatonic patterns)
- [x] Module 3 — Lick library data model + viewer + in-app authoring UI
      (create/edit/delete)
- [x] Module 4 — Picking technique engine (6 techniques) + Web Audio BPM
      tracker
- [x] Genre tagging/filtering across all modules, with presets that
      auto-fill sensible generator params
- [x] Functional/musical-accuracy review — done per-module as each one was
      built, not a single end-of-phase pass

## Phase 4 — Visualization ✅ done

- [x] SVG fretboard component (labels, sequence order, pick-direction,
      pluck-method), wired into all four module pages
- [x] AlphaTab integration (tab/staff notation) on all four module pages
- [x] Reviewed live by Jeremy (rhythm spacing, tab-number accuracy)

## Phase 5 — Responsive / PWA — not started

- [ ] Responsive layout (Tailwind breakpoints)
- [ ] PWA manifest / offline basics
- [ ] Test on actual desktop, tablet, and phone hardware (Jeremy)

## Phase 6 — Containerization — not started

- [ ] Finalize Dockerfile(s) + docker-compose for local dev — would also
      clean up local dev workflow (no more hand-managing the
      `guitar-guru-postgres` container)
- [ ] Build and run the container locally to confirm it works (Jeremy)

## Phase 7 — AWS Infrastructure — ON HOLD

Not started. Jeremy wants to address some items first (unspecified as of
2026-08-30) — don't start this phase until he gives the go-ahead.

- [ ] ECR repositor(y/ies)
- [ ] Three ECS Express Mode services (dev/qa/prod)
- [ ] Security groups so ECS reaches RDS
- [ ] Secrets Manager/SSM entries for DB credentials

## Phase 8 — CI/CD Pipeline — not started

Depends on Phase 7 being live.

- [ ] GitHub Actions workflow (build → deploy-dev → deploy-qa → deploy-prod)
- [ ] GitHub repo secrets (AWS credentials/OIDC role)
- [ ] GitHub Environments (`dev`/`qa`/`prod`) with required reviewers
- [ ] Run a PR through the full pipeline end-to-end

## Phase 9 — Ongoing / Post-Launch

- [ ] Expand the curated lick library over time (real lick content — none
      exists yet beyond throwaway test entries used during review)
- [ ] Add new exercise types/generators as they come up
- [ ] Maintain/rotate AWS credentials, monitor costs (once live)

## Known simplifications / worth revisiting later

Flagged during development, reviewed and accepted by Jeremy, but worth
remembering if musical content ever looks off in these specific spots:

- **F# major spelling** (`backend/app/engine/theory.py`,
  `midi_to_pitch_name`): renders the raised 7th as "F" instead of the
  theoretically-correct "E#" — a deliberate simplification for Module 1's
  simple per-key sharp/flat table.
- **Economy/sweep picking stroke direction**
  (`backend/app/engine/picking_technique.py`,
  `DOWNSTROKE_CONTINUES_WHEN_STRING_NUMBER_DECREASES`): a single named
  constant driving both rules, reviewed and confirmed correct by Jeremy —
  flip it here if it ever looks backwards again.
- **Hybrid picking pick/finger split**: bass-half-of-range = pick,
  treble-half = finger — a simplified convention, not a universal one.
- **Jazz genre preset**: approximated with melodic minor scale / minor
  triad chord-type presets, since true altered-dominant/modal content isn't
  in engine scope.
