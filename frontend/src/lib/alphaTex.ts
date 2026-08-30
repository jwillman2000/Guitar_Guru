import type { NoteEvent } from '../types/exercise'

// Identity for now — our string numbering (1 = high E, 6 = low E) is
// believed to match AlphaTex's convention, but this was not reliably
// confirmed from the docs. Verified empirically before this file's first
// real use (see the Phase 4 plan); if AlphaTab renders strings reversed,
// fix it here in one place.
function toAlphaTexString(ourString: number): number {
  return ourString
}

const VALID_DURATIONS = [1, 2, 4, 8, 16, 32] as const

// durationBeats=1 (this app's convention for a quarter note) -> AlphaTex
// duration code 4. Snapped to the nearest valid power-of-two; hand-curated
// licks could in principle carry unusual values even though every
// generator today always stamps durationBeats: 1.
function toAlphaTexDuration(durationBeats: number): number {
  if (!(durationBeats > 0)) return 4
  const raw = 4 / durationBeats
  return VALID_DURATIONS.reduce((closest, candidate) =>
    Math.abs(Math.log2(candidate) - Math.log2(raw)) < Math.abs(Math.log2(closest) - Math.log2(raw))
      ? candidate
      : closest,
  )
}

export function notesToAlphaTex(title: string, notes: NoteEvent[]): string {
  const escapedTitle = title.replace(/"/g, '\\"')
  const beats = notes
    .map((note) => {
      const string = toAlphaTexString(note.position.string)
      const duration = toAlphaTexDuration(note.durationBeats)
      return `${note.position.fret}.${string}.${duration}`
    })
    .join(' ')
  return `\\title "${escapedTitle}".\n${beats}`
}
