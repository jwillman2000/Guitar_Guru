import { useState } from 'react'
import { Fretboard } from '../../components/fretboard/Fretboard'
import { TabViewer } from '../../components/tab/TabViewer'
import { TagChips } from '../../components/TagChips'
import { apiPost } from '../../lib/api'
import { BUILT_IN_GENRES } from '../../lib/genres'
import type { GeneratedDrill } from '../../types/exercise'

const KEYS = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'F', 'Bb', 'Eb', 'Ab', 'Db']

export function FretboardLiteracyPage() {
  const [key, setKey] = useState('C')
  const [stringMin, setStringMin] = useState(1)
  const [stringMax, setStringMax] = useState(6)
  const [fretMin, setFretMin] = useState(0)
  const [fretMax, setFretMax] = useState(15)
  const [count, setCount] = useState(8)
  const [genre, setGenre] = useState('')

  const [drill, setDrill] = useState<GeneratedDrill | null>(null)
  const [error, setError] = useState<string | null>(null)

  async function handleGenerate() {
    setError(null)
    setDrill(null)
    const body: Record<string, unknown> = {
      key,
      stringRange: [stringMin, stringMax],
      fretRange: [fretMin, fretMax],
      count,
      difficulty: 'standard',
    }
    if (genre) body.genre = genre

    try {
      const result = await apiPost<GeneratedDrill>('/api/v1/fretboard-literacy/generate', body)
      setDrill(result)
    } catch (err) {
      setError((err as Error).message)
    }
  }

  return (
    <section className="p-6">
      <h1 className="mb-4 text-2xl font-semibold">Fretboard Literacy</h1>
      <p className="mb-6 text-neutral-500">Note-identity drills across the fretboard.</p>

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
            <label className="mb-1 block text-sm font-medium">Genre (optional)</label>
            <select
              className="w-full rounded border border-neutral-300 p-2 dark:border-neutral-700 dark:bg-neutral-900"
              value={genre}
              onChange={(e) => setGenre(e.target.value)}
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
            <label className="mb-1 block text-sm font-medium">String Range</label>
            <div className="flex gap-1">
              <input
                type="number"
                min={1}
                max={6}
                className="w-16 rounded border border-neutral-300 p-2 dark:border-neutral-700 dark:bg-neutral-900"
                value={stringMin}
                onChange={(e) => setStringMin(Number(e.target.value))}
              />
              <input
                type="number"
                min={1}
                max={6}
                className="w-16 rounded border border-neutral-300 p-2 dark:border-neutral-700 dark:bg-neutral-900"
                value={stringMax}
                onChange={(e) => setStringMax(Number(e.target.value))}
              />
            </div>
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium">Fret Range</label>
            <div className="flex gap-1">
              <input
                type="number"
                min={0}
                max={15}
                className="w-16 rounded border border-neutral-300 p-2 dark:border-neutral-700 dark:bg-neutral-900"
                value={fretMin}
                onChange={(e) => setFretMin(Number(e.target.value))}
              />
              <input
                type="number"
                min={0}
                max={15}
                className="w-16 rounded border border-neutral-300 p-2 dark:border-neutral-700 dark:bg-neutral-900"
                value={fretMax}
                onChange={(e) => setFretMax(Number(e.target.value))}
              />
            </div>
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium">Count</label>
            <input
              type="number"
              min={1}
              max={30}
              className="w-24 rounded border border-neutral-300 p-2 dark:border-neutral-700 dark:bg-neutral-900"
              value={count}
              onChange={(e) => setCount(Number(e.target.value))}
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
          <div className="mb-4">
            <TabViewer title={drill.title} notes={drill.notes} />
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
