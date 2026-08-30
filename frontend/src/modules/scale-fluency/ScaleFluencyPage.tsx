import { useState } from 'react'
import { Fretboard } from '../../components/fretboard/Fretboard'
import { TagChips } from '../../components/TagChips'
import { apiPost } from '../../lib/api'
import { BUILT_IN_GENRES, GENRE_PRESETS } from '../../lib/genres'
import type { GeneratedDrill } from '../../types/exercise'

const KEYS = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'F', 'Bb', 'Eb', 'Ab', 'Db']
const SCALES = ['major', 'natural_minor', 'harmonic_minor', 'melodic_minor', 'major_pentatonic', 'minor_pentatonic']

export function ScaleFluencyPage() {
  const [key, setKey] = useState('C')
  const [scale, setScale] = useState('major')
  const [startString, setStartString] = useState(6)
  const [startFret, setStartFret] = useState(0)
  const [numStrings, setNumStrings] = useState(6)
  const [genre, setGenre] = useState('')

  const [drill, setDrill] = useState<GeneratedDrill | null>(null)
  const [error, setError] = useState<string | null>(null)

  function handleGenreChange(next: string) {
    setGenre(next)
    const preset = GENRE_PRESETS[next]
    if (preset?.scale) setScale(preset.scale)
  }

  async function handleGenerate() {
    setError(null)
    setDrill(null)
    const body: Record<string, unknown> = {
      key,
      scale,
      startString,
      startFret,
      numStrings,
      difficulty: 'standard',
    }
    if (genre) body.genre = genre

    try {
      const result = await apiPost<GeneratedDrill>('/api/v1/scale-fluency/generate', body)
      setDrill(result)
    } catch (err) {
      setError((err as Error).message)
    }
  }

  return (
    <section className="p-6">
      <h1 className="mb-4 text-2xl font-semibold">Scale Fluency</h1>
      <p className="mb-6 text-neutral-500">
        Position-crossing exercises beyond CAGED-box thinking.
      </p>

      <div className="mb-6 max-w-xl space-y-3">
        <div className="flex gap-3">
          <div className="flex-1">
            <label className="mb-1 block text-sm font-medium">Key</label>
            <select
              className="w-full rounded border border-neutral-300 p-2 dark:border-neutral-700 dark:bg-neutral-900"
              value={key}
              onChange={(e) => setKey(e.target.value)}
            >
              {KEYS.map((k) => (
                <option key={k} value={k}>
                  {k}
                </option>
              ))}
            </select>
          </div>
          <div className="flex-1">
            <label className="mb-1 block text-sm font-medium">Scale</label>
            <select
              className="w-full rounded border border-neutral-300 p-2 dark:border-neutral-700 dark:bg-neutral-900"
              value={scale}
              onChange={(e) => setScale(e.target.value)}
            >
              {SCALES.map((s) => (
                <option key={s} value={s}>
                  {s.replace('_', ' ')}
                </option>
              ))}
            </select>
          </div>
          <div className="flex-1">
            <label className="mb-1 block text-sm font-medium">Genre (optional)</label>
            <select
              className="w-full rounded border border-neutral-300 p-2 dark:border-neutral-700 dark:bg-neutral-900"
              value={genre}
              onChange={(e) => handleGenreChange(e.target.value)}
            >
              <option value="">None</option>
              {BUILT_IN_GENRES.map((g) => (
                <option key={g} value={g}>
                  {g}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="flex gap-3">
          <div>
            <label className="mb-1 block text-sm font-medium">Start String</label>
            <input
              type="number"
              min={1}
              max={6}
              className="w-24 rounded border border-neutral-300 p-2 dark:border-neutral-700 dark:bg-neutral-900"
              value={startString}
              onChange={(e) => setStartString(Number(e.target.value))}
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium">Start Fret</label>
            <input
              type="number"
              min={0}
              max={15}
              className="w-24 rounded border border-neutral-300 p-2 dark:border-neutral-700 dark:bg-neutral-900"
              value={startFret}
              onChange={(e) => setStartFret(Number(e.target.value))}
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium">Num Strings</label>
            <input
              type="number"
              min={1}
              max={6}
              className="w-24 rounded border border-neutral-300 p-2 dark:border-neutral-700 dark:bg-neutral-900"
              value={numStrings}
              onChange={(e) => setNumStrings(Number(e.target.value))}
            />
          </div>
        </div>

        <button onClick={handleGenerate} className="rounded bg-purple-600 px-4 py-2 text-white">
          Generate
        </button>
      </div>

      {error && <p className="mb-4 text-red-500">{error}</p>}

      {drill && (
        <div className="max-w-xl">
          <h2 className="mb-2 font-medium">{drill.title}</h2>
          <TagChips genreTags={drill.genreTags} techniqueTags={drill.techniqueTags} />
          <div className="mb-4">
            <Fretboard notes={drill.notes} />
          </div>
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-neutral-300 dark:border-neutral-700">
                <th className="py-1">String</th>
                <th className="py-1">Fret</th>
                <th className="py-1">Pitch</th>
              </tr>
            </thead>
            <tbody>
              {drill.notes.map((note, i) => (
                <tr key={i} className="border-b border-neutral-100 dark:border-neutral-800">
                  <td className="py-1">{note.position.string}</td>
                  <td className="py-1">{note.position.fret}</td>
                  <td className="py-1">{note.pitch}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  )
}
