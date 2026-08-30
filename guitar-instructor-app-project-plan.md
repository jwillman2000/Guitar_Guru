# Guitar Instructor App — Project Plan

Starting point: fully greenfield — no AWS resources, no repo, no code exist yet. Companion to `guitar-instructor-app-spec.md`, which this plan implements. When build begins, this plan will be decomposed into individual specs following spec-driven development.

Assignee key: **Jeremy** = requires your accounts/credentials/hands-on action. **Claude** = code, config, or content Claude produces for you to add/run.

---

## Phase 0 — Accounts & Local Environment (Greenfield Setup)

| Task | Assignee | Notes |
|---|---|---|
| Create AWS account | Jeremy | Root account; set a billing alert/budget immediately since this is new |
| Create an IAM admin user (not root) + enable MFA | Jeremy | Day-to-day AWS work should not use root credentials |
| Create GitHub account/organization (if needed) and the new repo | Jeremy | Empty repo to start |
| Install Docker Desktop locally | Jeremy | Needed to build/test containers before pushing |
| Install Node.js + a code editor locally | Jeremy | Needed to run the frontend/backend Claude scaffolds |
| Confirm ECS Express Mode task uses Graviton (ARM64) | Jeremy | Matches native Docker builds on the M5 MacBook Air (Apple Silicon/ARM64) — avoids cross-compilation and is cheaper than x86_64 Fargate |

## Phase 1 — Repo & Project Scaffold

| Task | Assignee | Notes |
|---|---|---|
| Scaffold React + Tailwind frontend structure | Claude | Initial folders/components for the 4 modules |
| Scaffold backend project (FastAPI) | Claude | Locked in — Python, for the math/theory engine and future audio-feature potential |
| Write initial Dockerfile(s) | Claude | Frontend + backend, or combined depending on final architecture |
| Push scaffold to GitHub repo | Jeremy | First commit to `main` |
| Set branch protection on `main` (require PR review) | Jeremy | This is gate #1 in the pipeline design |

## Phase 2 — Data Layer

| Task | Assignee | Notes |
|---|---|---|
| Design Postgres schema (exercises, licks, tags: genre/technique/position) | Claude | JSONB-friendly schema per the spec |
| Write migration scripts | Claude | |
| Write seed data / initial curated lick entries | Claude | Ongoing content work, starts here |
| Create RDS Postgres instance (db.t4g.micro) | Jeremy | AWS console, first real infra resource |
| Create `app_dev` / `app_qa` / `app_prod` databases on the instance | Jeremy | One instance, three logical DBs |
| Run migrations/seed against RDS | Jeremy | Using scripts Claude provides |

## Phase 3 — Core Modules (Build Order TBD)

| Task | Assignee | Notes |
|---|---|---|
| Fretboard note-mapping engine (Module 1) | Claude | Foundation other modules build on |
| Scale fluency generator (Module 2) | Claude | Position-crossing exercise logic |
| Lick library data model + viewer (Module 3) | Claude | Ties into Module 2 positions |
| Lick authoring UI (create/edit licks in-app) (Module 3) | Claude | Replaces the Swagger-only `POST /licks` entry point from the initial viewer pass — hand-curated entry should happen in-app, not via API docs |
| Picking/technique engine + BPM tracker (Module 4) | Claude | |
| Genre tagging/filtering across all modules | Claude | Cross-cutting per the spec |
| Functional review + musical accuracy feedback on each module | Jeremy | Your guitar expertise is the QA here |

## Phase 4 — Visualization

| Task | Assignee | Notes |
|---|---|---|
| SVG fretboard component | Claude | |
| Integrate AlphaTab | Claude | Confirmed via hands-on Playground review |
| Verify tab/fretboard accuracy against real playing knowledge | Jeremy | |

## Phase 5 — Responsive / PWA

| Task | Assignee | Notes |
|---|---|---|
| Responsive layout (Tailwind breakpoints) | Claude | |
| PWA manifest / offline basics | Claude | |
| Test on actual desktop, tablet, and phone hardware | Jeremy | Claude can't test on your physical devices |

## Phase 6 — Containerization

| Task | Assignee | Notes |
|---|---|---|
| Finalize Dockerfile(s) + docker-compose for local dev | Claude | |
| Build and run the container locally to confirm it works | Jeremy | Sanity check before touching AWS |

## Phase 7 — AWS Infrastructure (Greenfield Build-Out)

| Task | Assignee | Notes |
|---|---|---|
| Create ECR repositor(y/ies) for the Docker image(s) | Jeremy | Console or CLI commands Claude can provide |
| Create three ECS Express Mode services (dev/qa/prod) | Jeremy | AWS's recommended App Runner replacement (App Runner closed to new customers as of April 30, 2026); console-driven per the "no Terraform" decision |
| Configure security groups so ECS tasks reach RDS | Jeremy | Simpler than App Runner's old VPC-connector step, since Express Mode/Fargate tasks run natively in your VPC |
| Create Secrets Manager/SSM entries for DB credentials | Jeremy | |
| Provide exact CLI commands / console steps for the above | Claude | On request, as you work through each resource |

## Phase 8 — CI/CD Pipeline

| Task | Assignee | Notes |
|---|---|---|
| Write GitHub Actions workflow (build → deploy-dev → deploy-qa → deploy-prod) | Claude | Build-once-promote-same-artifact pattern per spec |
| Configure GitHub repo secrets (AWS credentials/OIDC role) | Jeremy | Needed for Actions to reach AWS |
| Create GitHub Environments (`dev`/`qa`/`prod`) with required reviewers | Jeremy | This is the approval-gate mechanic |
| Run a PR through the full pipeline end-to-end and approve each gate | Jeremy | First real test of the whole flow |

## Phase 9 — Ongoing / Post-Launch

| Task | Assignee | Notes |
|---|---|---|
| Expand the curated lick library over time | Jeremy (content) + Claude (entry drafting) | Hand-curated per the sourcing philosophy |
| Add new exercise types/generators as you think of them | Claude | On request |
| Maintain/rotate AWS credentials, monitor costs | Jeremy | Ongoing account hygiene |

---

## Future Phases (Not Scheduled)

Four post-V1 ideas are on the radar — "play it for me" audio feedback, a built-in metronome, a "bet you can't play this" challenge mode, and AI integration (shape not yet defined). None are scheduled or task-broken-down yet; see the "Future Enhancements" section in `guitar-instructor-app-spec.md` for the architectural considerations already factored into the V1 plan above (structured exercise reference data, accurate metronome scheduling, a clean exercise-generation API boundary).

All planning-stage decisions are now locked in: FastAPI backend, AlphaTab for tab rendering, and module build order as listed in Phase 3 (fretboard literacy → scale fluency → lick library → picking technique).
