import type { Genre } from '../types/exercise'

// Built-in presets from the spec; the tag system is extensible beyond these.
export const BUILT_IN_GENRES: Genre[] = ['metal', 'jazz', 'country']

// Sensible generator params per genre, per the spec's style associations
// (metal: harmonic/melodic minor, sweep/tremolo-heavy; jazz: altered/modal
// flavor approximated here with melodic minor, since true altered-dominant
// content isn't in engine scope yet; country: major pentatonic, hybrid
// picking). Each generate page applies only the fields relevant to its own
// form — e.g. Fretboard Literacy has no scale/chord field, so picking a
// genre there only tags the result, with no param auto-fill.
export const GENRE_PRESETS: Record<string, { scale?: string; chordType?: string }> = {
  metal: { scale: 'harmonic_minor', chordType: 'minor_triad' },
  jazz: { scale: 'melodic_minor', chordType: 'minor_triad' },
  country: { scale: 'major_pentatonic', chordType: 'major_triad' },
}
