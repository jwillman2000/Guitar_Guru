import type { NoteEvent } from '../../types/exercise'

const STRING_COUNT = 6
const FRET_COUNT = 15
const FRET_WIDTH = 48
const STRING_GAP = 24
const MARGIN = 24
const DOT_RADIUS = 12

interface FretboardProps {
  notes?: NoteEvent[]
}

// Letter+accidental only (octave dropped for space — the accompanying table
// always shows the full pitch with octave).
function shortPitch(pitch: string): string {
  return pitch.replace(/\d+$/, '')
}

export function Fretboard({ notes = [] }: FretboardProps) {
  const width = MARGIN * 2 + FRET_COUNT * FRET_WIDTH
  const height = MARGIN * 2 + (STRING_COUNT - 1) * STRING_GAP

  const stringY = (stringNum: number) => MARGIN + (stringNum - 1) * STRING_GAP
  const fretX = (fret: number) => MARGIN + fret * FRET_WIDTH

  // Dedupe by (string, fret), keeping the first occurrence's data and its
  // original sequence order — relevant for drills that repeat the same
  // position (e.g. tremolo), where a pile of overlapping identical circles
  // wouldn't add anything the table doesn't already show.
  const seen = new Map<string, { note: NoteEvent; order: number }>()
  notes.forEach((note, index) => {
    const key = `${note.position.string}:${note.position.fret}`
    if (!seen.has(key)) seen.set(key, { note, order: index + 1 })
  })
  const positions = [...seen.values()]

  return (
    <svg
      viewBox={`0 0 ${width} ${height}`}
      className="w-full text-neutral-400 dark:text-neutral-600"
      role="img"
      aria-label="Fretboard diagram"
    >
      {Array.from({ length: STRING_COUNT }, (_, i) => i + 1).map((stringNum) => (
        <line
          key={`string-${stringNum}`}
          x1={MARGIN}
          x2={width - MARGIN}
          y1={stringY(stringNum)}
          y2={stringY(stringNum)}
          stroke="currentColor"
          strokeWidth={1}
        />
      ))}

      {Array.from({ length: FRET_COUNT + 1 }, (_, i) => i).map((fret) => (
        <line
          key={`fret-${fret}`}
          x1={fretX(fret)}
          x2={fretX(fret)}
          y1={MARGIN}
          y2={height - MARGIN}
          stroke="currentColor"
          strokeWidth={fret === 0 ? 3 : 1}
        />
      ))}

      {positions.map(({ note, order }) => {
        // Fret 0 (open string) sits at the nut line itself — it has no
        // "box" to its left the way fretted notes do, so centering it the
        // same way as fret >= 1 would push it half off the left edge.
        const cx = note.position.fret === 0 ? MARGIN : fretX(note.position.fret) - FRET_WIDTH / 2
        const cy = stringY(note.position.string)
        const fill = note.pluckMethod === 'finger' ? 'fill-emerald-500' : 'fill-purple-500'
        return (
          <g key={`${note.position.string}:${note.position.fret}`}>
            <title>
              {note.pitch} — string {note.position.string}, fret {note.position.fret}
              {note.pickDirection ? `, ${note.pickDirection}stroke` : ''}
              {note.pluckMethod ? `, ${note.pluckMethod}` : ''}
            </title>
            <text x={cx} y={cy - DOT_RADIUS - 4} textAnchor="middle" fontSize={7} fill="currentColor">
              {order}
            </text>
            <circle cx={cx} cy={cy} r={DOT_RADIUS} className={fill} />
            <text
              x={cx}
              y={cy}
              textAnchor="middle"
              dominantBaseline="central"
              fontSize={9}
              fontWeight="bold"
              fill="white"
            >
              {shortPitch(note.pitch)}
            </text>
            {note.pickDirection && (
              <text x={cx} y={cy + DOT_RADIUS + 10} textAnchor="middle" fontSize={10} fill="currentColor">
                {note.pickDirection === 'down' ? '↓' : '↑'}
              </text>
            )}
          </g>
        )
      })}
    </svg>
  )
}
