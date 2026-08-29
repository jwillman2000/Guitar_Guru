# Guitar Instructor App — Project Constitution

## Preamble

This project serves two purposes at once: a genuinely useful, technically
accurate personal guitar practice tool, and a hands-on vehicle for learning
GitHub CI/CD, AWS infrastructure, and containerization — tools Jeremy oversees
professionally but doesn't build day-to-day. This constitution exists so that
as the build gets underway, decisions stay anchored to both purposes, and so
it's clear how to resolve it when they pull in different directions. It
governs `guitar-instructor-app-spec.md` and `guitar-instructor-app-project-plan.md`,
and should be amended deliberately, not drifted from silently.

## Article I — Musical Accuracy Is Non-Negotiable

- All fretboard note identity, scale content, lick transcriptions, and tab
  notation must be correct at an advanced-player level — never beginner-grade
  approximation.
- Jeremy's 30+ years of playing experience is the final authority on musical
  accuracy. Claude may generate or draft content; nothing is "done" until
  Jeremy has verified it.
- Content is never scraped from the internet. Only two sourcing paths exist:
  (a) hand-curated canonical licks, entered one at a time, and (b)
  deterministic rules-engine-generated drills (scale formulas, interval math,
  genre-flavored parameter presets). An LLM may help choose creative
  parameters for generated drills, but never freehands the actual notes,
  frets, or tab content.

## Article II — Scope Is Deliberately Bounded to the Learning Goal

- Infrastructure choices optimize for real, hands-on experience with the
  target tools — not for production-grade scale this single-user app will
  never need.
- Terraform/IaC is explicitly out of scope. Console- and CLI-driven
  infrastructure work is itself part of the point.
- Default to the simplest architecture that still delivers genuine experience
  with GitHub Actions, AWS compute/registry, and Docker. When an underlying
  service changes or is deprecated (as happened with App Runner), prefer the
  smallest viable adjustment that preserves the original learning intent, and
  surface the change explicitly rather than quietly re-architecting around it.

## Article III — Build Once, Promote the Same Artifact

- CI/CD reflects real dev → qa → prod practice: build the Docker image once
  per merge, tag it with the git SHA, and promote that exact artifact through
  environments. Never rebuild per stage.
- Every promotion gate (qa, prod) requires manual approval via GitHub
  Environments' required-reviewer mechanic, even with Jeremy as sole
  reviewer — the point is to feel the mechanics of a gated pipeline, not just
  to ship fast.

## Article IV — Division of Labor Is Explicit and Respected

- Claude produces code, configuration, content drafts, and CLI/console
  instructions.
- Jeremy holds all credentials and accounts, provisions cloud resources,
  makes the final call on musical accuracy, and performs verification that
  requires physical hardware or real playing knowledge.
- Claude doesn't assume account access it doesn't have, and doesn't treat a
  plan step as complete until its assigned owner has actually done it.

## Article V — Architect for Known Future Needs, Without Building Them Yet

- The V1 schema stores structured reference data (target notes, timing, fret
  positions) for every exercise and lick — not just rendering strings. This
  costs little now and is required later for performance-feedback scoring.
- Any metronome or timing logic, whenever it's built, uses the Web Audio
  API's look-ahead scheduling pattern from the start, not basic JS timers,
  since it will eventually anchor performance analysis.
- Exercise-generation logic stays behind a clean internal API boundary, so a
  future AI or audio-analysis layer can call into it without a rewrite.
- No infrastructure is added ahead of need. Mic access, audio storage, and
  analysis compute arrive when those features are actually built, not before.

## Article VI — AI Integration Respects a Legal and Philosophical Line

- Song-specific tab content is commercial, copyrighted material. Any
  natural-language song-lookup feature resolves exclusively against Jeremy's
  personal library of legally obtained Guitar Pro/MusicXML files — it never
  scrapes or fetches copyrighted transcriptions from the web.
- AI's role in this project is matching, parameterizing, and assisting —
  never sourcing copyrighted musical content.

## Article VII — Amendments

This document changes when the project's stack, scope, or sourcing
philosophy materially changes — an AWS service deprecation, a new module, a
shift in build order. Amendments should be made deliberately and reflected in
both this file and `CLAUDE.md` together, not left to drift apart.
