import { useEffect, useRef, useState } from 'react'
import { Fretboard } from '../../components/fretboard/Fretboard'
import { TabViewer } from '../../components/tab/TabViewer'
import { TagChips } from '../../components/TagChips'
import { apiPost } from '../../lib/api'
import { BUILT_IN_GENRES, GENRE_PRESETS } from '../../lib/genres'
import { createMetronome, type Metronome } from '../../lib/metronome'
import type { GeneratedDrill } from '../../types/exercise'

const KEYS = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'F', 'Bb', 'Eb', 'Ab', 'Db']
const SCALES = ['major', 'natural_minor', 'harmonic_minor', 'melodic_minor', 'major_pentatonic', 'minor_pentatonic']
const CHORD_TYPES = ['major_triad', 'minor_triad', 'diminished_triad']
const TECHNIQUES = [
  { value: 'alternate', label: 'Alternate Picking' },
  { value: 'economy', label: 'Economy Picking' },
  { value: 'tremolo', label: 'Tremolo Picking' },
  { value: 'string_skipping', label: 'String Skipping' },
  { value: 'sweep', label: 'Sweep Picking' },
  { value: 'hybrid', label: 'Hybrid Picking' },
]

const usesScale = (t: string) => ['alternate', 'economy', 'string_skipping', 'hybrid', 'tremolo'].includes(t)
const usesStringRange = (t: string) => ['alternate', 'economy', 'string_skipping', 'sweep', 'hybrid'].includes(t)

// Sensible per-technique numStrings default — switching techniques must
// reset this, otherwise a leftover value (e.g. 6, from alternate picking)
// combined with string-skipping's `skip` can produce an out-of-range string
// pattern instead of a working default.
const DEFAULT_NUM_STRINGS: Record<string, number> = {
  alternate: 6,
  economy: 6,
  string_skipping: 3,
  sweep: 5,
  hybrid: 6,
}

export function PickingTechniquePage() {
  const [technique, setTechnique] = useState('alternate')
  const [key, setKey] = useState('C')
  const [scale, setScale] = useState('major')
  const [chordType, setChordType] = useState('major_triad')
  const [startString, setStartString] = useState(6)
  const [startFret, setStartFret] = useState(0)
  const [numStrings, setNumStrings] = useState(6)
  const [string, setString] = useState(1)
  const [fret, setFret] = useState(0)
  const [skip, setSkip] = useState(2)
  const [repeatCount, setRepeatCount] = useState(8)
  const [genre, setGenre] = useState('')

  const [drill, setDrill] = useState<GeneratedDrill | null>(null)
  const [error, setError] = useState<string | null>(null)

  const [bpm, setBpm] = useState(80)
  const [isPlaying, setIsPlaying] = useState(false)
  const metronomeRef = useRef<Metronome | null>(null)

  useEffect(() => {
    return () => {
      metronomeRef.current?.stop()
    }
  }, [])

  useEffect(() => {
    metronomeRef.current?.setBpm(bpm)
  }, [bpm])

  function toggleMetronome() {
    if (!metronomeRef.current) {
      metronomeRef.current = createMetronome(bpm)
    }
    if (isPlaying) {
      metronomeRef.current.stop()
      setIsPlaying(false)
    } else {
      metronomeRef.current.start()
      setIsPlaying(true)
    }
  }

  function handleGenreChange(next: string) {
    setGenre(next)
    const preset = GENRE_PRESETS[next]
    if (!preset) return
    if (preset.scale && usesScale(technique)) setScale(preset.scale)
    if (preset.chordType && technique === 'sweep') setChordType(preset.chordType)
  }

  async function handleGenerate() {
    setError(null)
    setDrill(null)
    const body: Record<string, unknown> = { technique, key, difficulty: 'standard' }
    if (usesScale(technique)) body.scale = scale
    if (technique === 'sweep') body.chordType = chordType
    if (usesStringRange(technique)) {
      body.startString = startString
      body.startFret = startFret
      body.numStrings = numStrings
    }
    if (technique === 'string_skipping') body.skip = skip
    if (technique === 'tremolo') {
      body.string = string
      body.fret = fret
      body.repeatCount = repeatCount
    }
    if (genre) body.genre = genre

    try {
      const result = await apiPost<GeneratedDrill>('/api/v1/picking-technique/generate', body)
      setDrill(result)
    } catch (err) {
      setError((err as Error).message)
    }
  }

  return (
    <section className="p-6">
      <h1 className="mb-4 text-2xl font-semibold">Picking Technique</h1>
      <p className="mb-6 text-neutral-500">
        Alternate/economy/sweep picking, string-skipping, hybrid picking, and tremolo, paired
        with a BPM tracker.
      </p>

      <div className="mb-6 max-w-xl space-y-3">
        <div>
          <label className="mb-1 block text-sm font-medium">Technique</label>
          <select
            className="w-full rounded border border-neutral-300 p-2 dark:border-neutral-700 dark:bg-neutral-900"
            value={technique}
            onChange={(e) => {
              const next = e.target.value
              setTechnique(next)
              if (DEFAULT_NUM_STRINGS[next] !== undefined) setNumStrings(DEFAULT_NUM_STRINGS[next])
              if (next === 'string_skipping') setStartString(6)
            }}
          >
            {TECHNIQUES.map((t) => (
              <option key={t.value} value={t.value}>
                {t.label}
              </option>
            ))}
          </select>
        </div>

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

          {usesScale(technique) && (
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
          )}

          {technique === 'sweep' && (
            <div className="flex-1">
              <label className="mb-1 block text-sm font-medium">Chord</label>
              <select
                className="w-full rounded border border-neutral-300 p-2 dark:border-neutral-700 dark:bg-neutral-900"
                value={chordType}
                onChange={(e) => setChordType(e.target.value)}
              >
                {CHORD_TYPES.map((c) => (
                  <option key={c} value={c}>
                    {c.replace('_', ' ')}
                  </option>
                ))}
              </select>
            </div>
          )}

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

        {usesStringRange(technique) && (
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
              <label className="mb-1 block text-sm font-medium">
                {technique === 'string_skipping' ? 'String Count' : 'Num Strings'}
              </label>
              <input
                type="number"
                min={1}
                max={6}
                className="w-24 rounded border border-neutral-300 p-2 dark:border-neutral-700 dark:bg-neutral-900"
                value={numStrings}
                onChange={(e) => setNumStrings(Number(e.target.value))}
              />
            </div>
            {technique === 'string_skipping' && (
              <div>
                <label className="mb-1 block text-sm font-medium">Skip</label>
                <input
                  type="number"
                  min={2}
                  max={5}
                  className="w-24 rounded border border-neutral-300 p-2 dark:border-neutral-700 dark:bg-neutral-900"
                  value={skip}
                  onChange={(e) => setSkip(Number(e.target.value))}
                />
              </div>
            )}
          </div>
        )}

        {technique === 'tremolo' && (
          <div className="flex gap-3">
            <div>
              <label className="mb-1 block text-sm font-medium">String</label>
              <input
                type="number"
                min={1}
                max={6}
                className="w-24 rounded border border-neutral-300 p-2 dark:border-neutral-700 dark:bg-neutral-900"
                value={string}
                onChange={(e) => setString(Number(e.target.value))}
              />
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium">Fret</label>
              <input
                type="number"
                min={0}
                max={15}
                className="w-24 rounded border border-neutral-300 p-2 dark:border-neutral-700 dark:bg-neutral-900"
                value={fret}
                onChange={(e) => setFret(Number(e.target.value))}
              />
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium">Repeat Count</label>
              <input
                type="number"
                min={1}
                max={32}
                className="w-24 rounded border border-neutral-300 p-2 dark:border-neutral-700 dark:bg-neutral-900"
                value={repeatCount}
                onChange={(e) => setRepeatCount(Number(e.target.value))}
              />
            </div>
          </div>
        )}

        <button onClick={handleGenerate} className="rounded bg-purple-600 px-4 py-2 text-white">
          Generate
        </button>
      </div>

      {error && <p className="mb-4 text-red-500">{error}</p>}

      {drill && (
        <div className="mb-8 max-w-xl">
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
                <th className="py-1">Pick / Finger</th>
              </tr>
            </thead>
            <tbody>
              {drill.notes.map((note, i) => (
                <tr key={i} className="border-b border-neutral-100 dark:border-neutral-800">
                  <td className="py-1">{note.position.string}</td>
                  <td className="py-1">{note.position.fret}</td>
                  <td className="py-1">{note.pitch}</td>
                  <td className="py-1">
                    {note.pickDirection === 'down' ? '↓' : note.pickDirection === 'up' ? '↑' : ''}
                    {note.pluckMethod ?? ''}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <div className="max-w-xl rounded border border-neutral-300 p-4 dark:border-neutral-700">
        <h2 className="mb-2 font-medium">BPM Tracker</h2>
        <div className="flex items-center gap-3">
          <input
            type="number"
            min={20}
            max={300}
            className="w-24 rounded border border-neutral-300 p-2 dark:border-neutral-700 dark:bg-neutral-900"
            value={bpm}
            onChange={(e) => setBpm(Number(e.target.value))}
          />
          <span className="text-sm text-neutral-500">BPM</span>
          <button
            onClick={toggleMetronome}
            className="rounded bg-purple-600 px-4 py-2 text-white"
          >
            {isPlaying ? 'Stop' : 'Start'}
          </button>
        </div>
      </div>
    </section>
  )
}
