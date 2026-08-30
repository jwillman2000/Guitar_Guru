// Shared shape for exercises/licks across all four modules.
// Mirrors the backend schema: structured reference data (notes, timing,
// fret positions), not just a rendering string — see CONSTITUTION.md Article V.

export type Genre = 'metal' | 'jazz' | 'country' | (string & {})

export type Technique =
  | 'alternate-picking'
  | 'economy-picking'
  | 'sweep-picking'
  | 'string-skipping'
  | 'hybrid-picking'
  | 'tremolo'

export interface FretPosition {
  string: number // 1 (high E) – 6 (low E)
  fret: number
}

export interface NoteEvent {
  position: FretPosition
  pitch: string // e.g. "G4", spelled per key context
  startBeat: number
  durationBeats: number
}

export interface ExerciseBase {
  id: string
  title: string
  genreTags: Genre[]
  techniqueTags: Technique[]
  notes: NoteEvent[]
}

export interface GeneratedDrill extends ExerciseBase {
  source: 'generated'
  moduleId: 'fretboard-literacy' | 'scale-fluency' | 'picking-technique'
  generatorParams: Record<string, unknown>
}

export interface CanonicalLick extends ExerciseBase {
  source: 'canonical'
  moduleId: 'lick-library'
  artist: string | null
  song: string
  key: string
  difficulty: string
  description: string | null
  scalePositions: number[] // positions this lick crosses, ties back to Module 2
}

export type Exercise = GeneratedDrill | CanonicalLick
