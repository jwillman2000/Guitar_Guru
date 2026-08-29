# Guitar Instructor App — Planning Spec

Status: idea/spec phase, not yet building. When build begins, this plan will be decomposed into individual specs following spec-driven development.

## Purpose

A personal guitar practice application for an advanced player (30+ years, high technical/musical knowledge) needing targeted, non-beginner training — not generic lesson content.

## Core Modules

1. **Fretboard Literacy** — exercises teaching actual note *identity* across the fretboard (not just fret numbers), with enharmonic spelling that adjusts to key context.
2. **Scale Fluency** — exercises designed to break out of standard CAGED-box thinking: 3-notes-per-string groupings, connecting adjacent positions across shifts, single scale confined to 2 strings across the whole neck, etc.
3. **Lick Library** — curated collection of well-known/iconic licks, tagged so they tie back into Module 2 (e.g., a G minor pentatonic lick that crosses 3 scale positions, with the fretboard/tab showing *why* it crosses positions).
4. **Right-Hand / Picking Technique** — alternate picking, economy picking, sweep picking, string-skipping, hybrid picking, tremolo — paired with a metronome/BPM tracker to measure and progress speed over time.

## Genre Filtering (cross-cutting, not a separate module)

A tagging system across all four modules so exercises can be requested by genre feel:
- **Metal** — harmonic/melodic minor, diminished, tritone-heavy phrasing, tremolo/sweep-heavy picking patterns.
- **Jazz** — arpeggios over changes, chromatic approach tones, altered dominants, swing-feel picking.
- **Country** — major pentatonic with bends, hybrid picking / chicken pickin'.
- Extensible to other genres via the same tag system.

## Exercise Sourcing Philosophy

No scraping/sourcing exercises from the internet. Two distinct content paths instead:
- **Canonical licks** (Module 3): hand-curated, built entry by entry — a famous lick is a fixed, specific thing that can't be reliably auto-sourced with correct notes.
- **Generated drills** (Modules 1, 2, 4): produced by a deterministic, rules-based music-theory engine in code (scale formulas, interval math, genre-flavored parameter presets) — not free-form AI text generation, since exact fret/note correctness matters. An LLM could assist in picking creative parameters, but the engine outputs the actual notes/frets.

## Frontend

- React + Tailwind, built as a single responsive PWA (not separate native apps) to cover desktop, tablet, and phone from one codebase.
- Fretboard diagrams: SVG component (scales/note highlights are straightforward to render and animate this way).
- Tab notation: **AlphaTab** — confirmed via hands-on evaluation of the official Playground (purpose-built for guitar tab, responsive, handles the position-shift/lick visualization needs).

## Backend & Data

- Backend required (not purely client-side) since the app will be containerized and hosted: **FastAPI (Python)** — chosen for the stronger ecosystem for scale/interval math and potential future audio features (pitch detection, tuner), automatic request validation/OpenAPI docs, and as a deliberate opportunity to gain Python experience.
- Database: single small **RDS Postgres** instance (e.g. db.t4g.micro) — skip Aurora Serverless (non-zero minimum cost not worth it for one user). Postgres with JSONB fits the flexible, multi-tag exercise/lick metadata (key, scale, position, genre, technique).
- Three logical databases on the one instance: `app_dev`, `app_qa`, `app_prod` — rather than three separate instances, to keep cost down.

## Hosting & Infra (AWS, Docker)

Context: single user, no horizontal scaling needed, goal is general hands-on AWS/CI-CD/Docker experience (not deep expertise — e.g. deliberately skipping Terraform/IaC since that's not part of his day-to-day responsibilities).

- **Compute:** Amazon **ECS Express Mode** — AWS's official recommended replacement for App Runner (App Runner closed to new customers as of April 30, 2026). Provisions Fargate compute, ALB, HTTPS, auto-scaling, and an auto-generated domain from just a container image + IAM roles — preserves App Runner-like simplicity while being part of the broader ECS ecosystem.
- **Architecture: Graviton (ARM64)** — dev machine is an Apple Silicon Mac (M5), which builds ARM64 Docker images natively. Configuring the Fargate task definition for Graviton/ARM64 (rather than the x86_64 default) matches local builds with no cross-compilation, and Graviton Fargate pricing also runs cheaper than x86_64.
- **Three ECS Express Mode services:** `dev`, `qa`, `prod` — Express Mode can consolidate up to 25 services behind a single shared ALB, avoiding the cost of three separate load balancers.
- **Database connectivity:** ECS Express Mode runs on Fargate, so tasks live natively in your VPC (no separate connector needed, unlike App Runner) — reach RDS via standard security group rules; fallback is a publicly reachable RDS instance locked to his IP if needed.
- **Images:** stored in **ECR**.
- **Secrets:** Secrets Manager or SSM Parameter Store for DB credentials — not baked into the image or plain env vars.
- **Domain/HTTPS:** Express Mode auto-provisions both.
- **No Terraform/CDK** — console, CLI, or Express Mode's guided setup is the intended approach; infra-as-code isn't a gap he needs to fill for this project.

## CI/CD & Environment Promotion (GitHub)

Goal: replicate a real dev → qa → prod quality-gated pipeline, even as sole approver, to get a feel for how a PR travels through gates.

- **Branching:** feature branches → PR into `main` (PR review is itself gate #1, even as sole reviewer).
- **Pipeline (GitHub Actions), triggered on merge to `main`:**
  1. `build` — build Docker image once, tag with git SHA, push to ECR once.
  2. `deploy-dev` — deploy that same image to the `dev` ECS Express Mode service, auto-triggered.
  3. `deploy-qa` — gated by GitHub **Environments** required-reviewer protection rule; deploy same image to `qa` after manual approval.
  4. `deploy-prod` — same gating pattern, deploy to `prod` after manual approval.
  - Jobs chained via `needs:` so qa/prod jobs wait on prior stages.
- **Key principle:** build once, promote the same artifact through dev/qa/prod rather than rebuilding per stage — matches real-world practice of testing the exact artifact that ships.
- **Gate mechanic:** GitHub repo Settings → Environments → create `dev`/`qa`/`prod`, add required reviewers (himself) to `qa` and `prod`. Workflow runs pause with a "Review deployments" button until approved.

## Future Enhancements (Not in V1 Scope)

Captured now so early architecture doesn't foreclose them later — none of this is scheduled or scoped for the initial build.

1. **"Play it for me" (performance feedback)** — user plays a lick/exercise, the app listens via microphone and evaluates timing and intonation accuracy (including bends). Would require mic capture (Web Audio API), a pitch-detection approach (likely feasible server-side via Python audio libraries like librosa/aubio, pairing well with the FastAPI backend), and structured reference data per exercise (expected pitch/timing sequence, not just a tab string).
2. **Built-in metronome** — supports #1 as a shared timing reference, plus standalone practice use.
3. **"Bet you can't play this" challenge mode** — an extreme-difficulty tag within the Lick Library/generator; could tie into #1 later for scored attempts.
4. **AI integration** — not yet fully defined, but with a concrete first example in mind: natural-language song lookup (e.g., "teach me the outro solo of Stairway to Heaven") that resolves to a specific song/section and renders it for practice at adjustable speed. Also possible: natural-language exercise requests (interpreted into the rules-based generator's parameters) or AI-assisted feedback layered on top of #1's raw analysis.

### Implications for V1 build decisions
- Design the exercise/lick database schema to store structured reference data (target notes, timing, fret positions), not just rendering strings — useful now for animation/playback, needed later for scoring.
- Build the metronome, whenever it's built, using the Web Audio API's look-ahead scheduling pattern rather than basic JS timers, since accuracy matters once it underlies timing analysis.
- Keep exercise-generation logic behind a clean internal API boundary so a future AI or audio-analysis layer can call into it without a rewrite.
- No infrastructure changes needed for V1 — mic access, audio storage, and any added compute for pitch analysis can be introduced when those features are actually built.
- Song-specific tabs (as opposed to original hand-curated licks) are commercial/copyrighted content. The sourcing approach for the song-lookup AI example above should be a personal file-import pipeline — legally obtained Guitar Pro/MusicXML files added to a personal library — rather than scraping tab sites; the AI's role is matching a request to that personal catalog, not fetching copyrighted transcriptions from the web.
- AlphaTab already supports importing Guitar Pro/MusicXML files and has built-in playback speed control and looping — so slowed-down practice playback for a learned song is largely covered by the already-chosen library rather than requiring new engineering.
