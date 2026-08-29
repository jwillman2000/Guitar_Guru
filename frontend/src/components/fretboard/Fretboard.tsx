import type { FretPosition } from '../../types/exercise'

// Minimal SVG fretboard scaffold. Full rendering (note-name labels, enharmonic
// spelling, animation) is Phase 4 work — this establishes the component shape
// and coordinate system the modules will render highlights onto.

const STRING_COUNT = 6
const FRET_COUNT = 15
const FRET_WIDTH = 48
const STRING_GAP = 24
const MARGIN = 24

interface FretboardProps {
  highlights?: FretPosition[]
}

export function Fretboard({ highlights = [] }: FretboardProps) {
  const width = MARGIN * 2 + FRET_COUNT * FRET_WIDTH
  const height = MARGIN * 2 + (STRING_COUNT - 1) * STRING_GAP

  const stringY = (stringNum: number) => MARGIN + (stringNum - 1) * STRING_GAP
  const fretX = (fret: number) => MARGIN + fret * FRET_WIDTH

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

      {highlights.map(({ string, fret }, i) => (
        <circle
          key={i}
          cx={fretX(fret) - FRET_WIDTH / 2}
          cy={stringY(string)}
          r={9}
          className="fill-purple-500"
        />
      ))}
    </svg>
  )
}
