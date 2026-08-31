# Project Diary — Guitar Guru

Source material for a Substack post on what building this app with Claude
Code taught me — about AWS, CI/CD, Docker, and working with an AI agent on
a real, multi-session project. Not a polished narrative — a factual log of
what got built, the decisions behind it, and the specific moments (bugs,
pivots, near-misses) worth mining for the actual write-up.

Covers 2026-08-29 through 2026-08-31 (three sessions so far). All work
merged via PR #1–#11 on GitHub; nothing has touched AWS yet.

---

## The setup

Personal guitar practice app (4 modules: Fretboard Literacy, Scale Fluency,
Lick Library, Picking Technique), doubling as a hands-on vehicle for
learning AWS, CI/CD, and Docker. Stack locked in early: React/Tailwind
frontend, FastAPI backend, one RDS Postgres instance with three logical
databases, ECS Express Mode for compute, GitHub Actions for CI/CD — all
documented in `CLAUDE.md`/`CONSTITUTION.md` before any code was written.

**Early decision point worth noting:** I asked whether to let Claude
directly manage AWS via an "Agent Toolkit" MCP server (AWS CLI + browser
auth) rather than hand-copying console/CLI instructions back and forth. I
declined — deliberately preserving the human-in-the-loop boundary the
project's own constitution set up (Claude writes code/config, Jeremy holds
all credentials and does all provisioning). Worth reflecting on in the
post: the tooling to hand an AI agent real cloud access already exists and
is easy to set up — the harder question is whether you want to.

## Phase 0–1: Scaffold

- React + Tailwind frontend scaffold, FastAPI backend scaffold, initial
  Dockerfiles, pushed to GitHub with branch protection on `main`.
- Established the working pattern used for the rest of the project: every
  change lands on a feature branch, goes through a real PR, gets reviewed
  (by me for musical/functional accuracy, informally by Claude for code
  quality), then merged — even for a one-person project. Small PRs, ~11 of
  them by the end of this diary's window.

## Phase 2: Data Layer

- Postgres schema for exercises/licks/tags (JSONB-friendly, structured
  reference data rather than just rendering strings — decided up front so
  future features like performance scoring wouldn't need a schema rewrite).
- **A concrete AWS console gotcha**: went to create the RDS instance and
  initially ended up with an Aurora Serverless cluster instead of a plain
  `db.t4g.micro` RDS Postgres instance — the console's "Easy configuration"
  path defaults toward Aurora without making that obvious. Had to delete
  and recreate with "Full configuration" instead. Small thing, but a real
  example of how an AWS console default can quietly steer you somewhere
  you didn't intend.
- **A password ended up in the chat transcript** at one point (pasted
  directly into a shell command instead of into an interactive prompt).
  Flagged it immediately and rotated the RDS master password afterward.
  Worth a mention in the post as a real "AI agent sees your terminal"
  hygiene lesson — treat anything typed into a command as effectively
  exposed.
- Idempotent tag-taxonomy seed script (genre/technique/position tags).

## Phase 3: Core Modules

Built in the fixed order the spec called for: Fretboard Literacy → Scale
Fluency → Lick Library → Picking Technique.

- **Module 1 (Fretboard Literacy)** — deterministic MIDI-based note-mapping
  engine, spelling notes correctly per key (sharps vs. flats). Flagged one
  known simplification openly rather than silently: F# major's raised 7th
  renders as "F" instead of the theoretically-correct "E#". Reviewed and
  accepted.
- **Module 2 (Scale Fluency)** — 3-notes-per-string pattern generator.
  **Real bug caught during design, before any code shipped**: the first
  approach would have spelled minor scales using the *major* key's
  sharp/flat convention, which is wrong for minor keys generally and
  actively broken for harmonic/melodic minor's raised leading tone in flat
  keys. Fixed with a more rigorous letter-by-letter spelling algorithm
  instead of a coarse per-key table. Later extended to add pentatonic
  scales as a follow-up once the base pattern was validated.
- **Module 3 (Lick Library)** — data model, API, and a read-only viewer
  first. **A requirements-surfaced-by-using-it moment**: after trying it,
  I pushed back that content should be addable *in the app*, not just via
  the API's Swagger docs. That became its own follow-up PR: full
  create/edit/delete UI, plus the `PUT`/`DELETE` endpoints that hadn't
  existed yet. A good example of a gap that only became obvious by
  actually clicking around, not by reading a spec.
- **Module 4 (Picking Technique + BPM tracker)** — six picking techniques
  (alternate, economy, tremolo, string skipping, sweep, hybrid) plus a
  Web Audio metronome.
  - **A documented-constraint conflict surfaced here**: the project's own
    "Deferred — Not V1" list explicitly ruled out a standalone metronome,
    but the phase plan called for a "BPM tracker" in this same module.
    Resolved by scoping it as a drill-specific click track embedded in the
    page, not a general reusable metronome — satisfies both.
  - **A genuine "I don't know" moment, handled explicitly rather than
    guessed past**: economy-picking and sweep-picking direction depends on
    a physical pick-motion convention that wasn't reliably derivable from
    memory alone. Rather than assert it confidently, it got isolated into
    one named, heavily-commented constant so a wrong guess would be a
    one-line fix, not a scattered one — then reviewed and confirmed
    correct against real playing experience.
  - **A real bug caught by actually running the code**: an early version
    of the note-generation algorithm produced negative fret numbers for
    certain one-note-per-string patterns. Not caught by reading the code —
    caught by generating a drill and seeing the error.
  - Web Audio look-ahead scheduling for the metronome (the "two clocks"
    pattern — a low-frequency timer only re-checks a schedule window;
    actual click timing comes from the audio clock). Verified after the
    fact by patching the browser's own oscillator API during a test run
    and measuring the actual scheduled intervals: zero timing error.
- **Genre tagging** — cross-cutting feature (Metal/Jazz/Country presets
  that auto-fill sensible scale/technique parameters). Building this
  properly meant giving Fretboard Literacy and Scale Fluency real
  generate-and-display frontend pages for the first time — they'd been
  Swagger-only up to that point. Pulled a bit of Phase 4 frontend work
  earlier than planned, deliberately, because it made the feature land
  consistently everywhere at once instead of half-finished.

## Phase 4: Visualization

- **SVG fretboard component** — upgraded from a bare dot-scaffold to show
  note labels, play-order numbers, pick-direction arrows, and pick/finger
  color coding, then wired into all four modules at once (it had actually
  gone unused for a while — the generator pages had shipped with plain
  tables instead, since the component wasn't good enough yet to bother
  with). **Bug caught by actually looking at the screenshot**: open-string
  notes were rendering half-clipped off the left edge of the diagram — a
  coordinate-math edge case (fret 0 has no "box" to its left the way
  fretted notes do) that was invisible in the code and obvious in a
  rendered screenshot.
- **AlphaTab integration** — real tab/staff notation, not just a
  placeholder. Two things worth calling out:
  - **A dev-only bug**: the library's font failed to load specifically
    under the Vite dev server (worked fine in a production build) because
    its own path auto-detection isn't reliable there. One explicit config
    line fixed it — but it's the kind of "works in prod, fails in dev"
    issue that's easy to miss if you only ever test the built artifact.
  - **An assumption verified empirically instead of trusted on faith**:
    whether the library's string-numbering convention matched this app's
    own wasn't clearly documented anywhere findable. Rather than guess,
    rendered one unambiguous known note and visually confirmed it landed
    correctly before wiring up the real converter. It matched — but the
    point is checking rather than assuming.

## Process notes (for the "how I worked with Claude" part of the post)

- Every non-trivial feature went through the same loop: explore the
  existing code first, write an explicit plan (including open questions),
  get it approved *before* writing code, implement, write tests, verify
  behavior in a real browser (via automated Chromium sessions, not just
  "looks right"), then hand it over for review before merging.
- Real bugs got caught at almost every stage of that loop — some in
  design (the minor-key spelling issue), some by running tests (the
  negative-fret bug), some only by looking at a rendered screenshot (the
  fretboard clipping bug, the AlphaTab font issue). No single stage caught
  everything; the combination did.
- Uncertainty got flagged explicitly instead of papered over — the pick
  direction convention, the F# spelling simplification, the jazz genre
  preset being an approximation. Each is logged in `tasks.md` under "known
  simplifications" specifically so they don't quietly get forgotten.
- `tasks.md` (phase checklist) and this diary are themselves an artifact
  of working sporadically on a side project — external memory for picking
  the thread back up across days, not just for the AI but for me.

## Where things stand

Phases 0–4 done. Phase 5 (Responsive/PWA) and Phase 6 (Containerization)
are next, both still local-only. AWS deployment (Phase 7) and the CI/CD
pipeline (Phase 8) are intentionally on hold — I have some things to sort
out before pushing this to real infrastructure.
