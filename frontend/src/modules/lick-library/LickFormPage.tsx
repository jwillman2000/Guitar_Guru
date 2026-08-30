import { useEffect, useState, type FormEvent } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { apiGet, apiPost, apiPut } from '../../lib/api'
import type { CanonicalLick, NoteEvent } from '../../types/exercise'
import type { Tag } from '../../types/tag'

const POSITIONS = [1, 2, 3, 4, 5]

function emptyNote(): NoteEvent {
  return { position: { string: 6, fret: 0 }, pitch: '', startBeat: 0, durationBeats: 1 }
}

export function LickFormPage() {
  const { id } = useParams<{ id: string }>()
  const isEditing = id !== undefined
  const navigate = useNavigate()

  const [tags, setTags] = useState<Tag[] | null>(null)
  const [loadError, setLoadError] = useState<string | null>(null)
  const [submitError, setSubmitError] = useState<string | null>(null)

  const [title, setTitle] = useState('')
  const [artist, setArtist] = useState('')
  const [song, setSong] = useState('')
  const [key, setKey] = useState('')
  const [difficulty, setDifficulty] = useState('standard')
  const [description, setDescription] = useState('')
  const [notes, setNotes] = useState<NoteEvent[]>([emptyNote()])
  const [selectedTagIds, setSelectedTagIds] = useState<number[]>([])
  const [selectedPositions, setSelectedPositions] = useState<number[]>([])

  useEffect(() => {
    apiGet<Tag[]>('/api/v1/tags/')
      .then(setTags)
      .catch((err: Error) => setLoadError(err.message))
  }, [])

  const [loadedLick, setLoadedLick] = useState<CanonicalLick | null>(null)

  useEffect(() => {
    if (!isEditing) return
    apiGet<CanonicalLick>(`/api/v1/licks/${id}`)
      .then((lick) => {
        setLoadedLick(lick)
        setTitle(lick.title)
        setArtist(lick.artist ?? '')
        setSong(lick.song)
        setKey(lick.key)
        setDifficulty(lick.difficulty)
        setDescription(lick.description ?? '')
        setNotes(lick.notes.length > 0 ? lick.notes : [emptyNote()])
        setSelectedPositions(lick.scalePositions)
        // Tag IDs aren't in the lick response (only names) — resolved once tags load, below.
      })
      .catch((err: Error) => setLoadError(err.message))
  }, [id, isEditing])

  useEffect(() => {
    if (!loadedLick || !tags) return
    const ids = tags
      .filter(
        (t) =>
          (t.category === 'genre' && loadedLick.genreTags.includes(t.name)) ||
          (t.category === 'technique' && loadedLick.techniqueTags.includes(t.name)),
      )
      .map((t) => t.id)
    setSelectedTagIds(ids)
  }, [loadedLick, tags])

  function updateNote(index: number, patch: Partial<NoteEvent> | Partial<NoteEvent['position']>) {
    setNotes((prev) =>
      prev.map((note, i) =>
        i === index
          ? 'string' in patch || 'fret' in patch
            ? { ...note, position: { ...note.position, ...patch } }
            : { ...note, ...patch }
          : note,
      ),
    )
  }

  function toggleTag(tagId: number) {
    setSelectedTagIds((prev) => (prev.includes(tagId) ? prev.filter((id_) => id_ !== tagId) : [...prev, tagId]))
  }

  function togglePosition(position: number) {
    setSelectedPositions((prev) => (prev.includes(position) ? prev.filter((p) => p !== position) : [...prev, position]))
  }

  // In edit mode, the loaded lick's data arrives asynchronously after the form
  // shell renders — gate on it so a user can't start typing into fields that
  // are about to be overwritten once the fetch resolves.
  const isReady = !isEditing || loadedLick !== null
  const canSubmit = title.trim() !== '' && song.trim() !== '' && key.trim() !== '' && notes.length > 0

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setSubmitError(null)

    const body = {
      title,
      artist: artist.trim() === '' ? null : artist,
      song,
      key,
      difficulty,
      description: description.trim() === '' ? null : description,
      notes,
      tagIds: selectedTagIds,
      scalePositions: selectedPositions,
    }

    try {
      const result = isEditing
        ? await apiPut<CanonicalLick>(`/api/v1/licks/${id}`, body)
        : await apiPost<CanonicalLick>('/api/v1/licks/', body)
      navigate(`/lick-library/${result.id}`)
    } catch (err) {
      setSubmitError((err as Error).message)
    }
  }

  const genreTags = tags?.filter((t) => t.category === 'genre') ?? []
  const techniqueTags = tags?.filter((t) => t.category === 'technique') ?? []

  return (
    <section className="p-6">
      <h1 className="mb-4 text-2xl font-semibold">{isEditing ? 'Edit Lick' : 'Add Lick'}</h1>

      {loadError && <p className="text-red-500">Failed to load: {loadError}</p>}
      {!loadError && !isReady && <p className="text-neutral-500">Loading…</p>}

      {isReady && (
      <form onSubmit={handleSubmit} className="max-w-2xl space-y-4">
        <div>
          <label className="mb-1 block text-sm font-medium">Title</label>
          <input
            className="w-full rounded border border-neutral-300 p-2 dark:border-neutral-700 dark:bg-neutral-900"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
        </div>
        <div>
          <label className="mb-1 block text-sm font-medium">Song</label>
          <input
            className="w-full rounded border border-neutral-300 p-2 dark:border-neutral-700 dark:bg-neutral-900"
            value={song}
            onChange={(e) => setSong(e.target.value)}
          />
        </div>
        <div>
          <label className="mb-1 block text-sm font-medium">Artist</label>
          <input
            className="w-full rounded border border-neutral-300 p-2 dark:border-neutral-700 dark:bg-neutral-900"
            value={artist}
            onChange={(e) => setArtist(e.target.value)}
          />
        </div>
        <div className="flex gap-4">
          <div className="flex-1">
            <label className="mb-1 block text-sm font-medium">Key</label>
            <input
              className="w-full rounded border border-neutral-300 p-2 dark:border-neutral-700 dark:bg-neutral-900"
              value={key}
              onChange={(e) => setKey(e.target.value)}
              placeholder="e.g. E minor"
            />
          </div>
          <div className="flex-1">
            <label className="mb-1 block text-sm font-medium">Difficulty</label>
            <input
              className="w-full rounded border border-neutral-300 p-2 dark:border-neutral-700 dark:bg-neutral-900"
              value={difficulty}
              onChange={(e) => setDifficulty(e.target.value)}
            />
          </div>
        </div>
        <div>
          <label className="mb-1 block text-sm font-medium">Description</label>
          <textarea
            className="w-full rounded border border-neutral-300 p-2 dark:border-neutral-700 dark:bg-neutral-900"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </div>

        <div>
          <span className="mb-1 block text-sm font-medium">Genre tags</span>
          <div className="flex flex-wrap gap-3">
            {genreTags.map((tag) => (
              <label key={tag.id} className="flex items-center gap-1 text-sm">
                <input
                  type="checkbox"
                  checked={selectedTagIds.includes(tag.id)}
                  onChange={() => toggleTag(tag.id)}
                />
                {tag.name}
              </label>
            ))}
          </div>
        </div>

        <div>
          <span className="mb-1 block text-sm font-medium">Technique tags</span>
          <div className="flex flex-wrap gap-3">
            {techniqueTags.map((tag) => (
              <label key={tag.id} className="flex items-center gap-1 text-sm">
                <input
                  type="checkbox"
                  checked={selectedTagIds.includes(tag.id)}
                  onChange={() => toggleTag(tag.id)}
                />
                {tag.name}
              </label>
            ))}
          </div>
        </div>

        <div>
          <span className="mb-1 block text-sm font-medium">Scale Fluency positions crossed</span>
          <div className="flex flex-wrap gap-3">
            {POSITIONS.map((position) => (
              <label key={position} className="flex items-center gap-1 text-sm">
                <input
                  type="checkbox"
                  checked={selectedPositions.includes(position)}
                  onChange={() => togglePosition(position)}
                />
                Position {position}
              </label>
            ))}
          </div>
        </div>

        <div>
          <span className="mb-2 block text-sm font-medium">Notes</span>
          <div className="space-y-2">
            {notes.map((note, index) => (
              <div key={index} className="flex flex-wrap items-center gap-2">
                <input
                  type="number"
                  min={1}
                  max={6}
                  className="w-16 rounded border border-neutral-300 p-1 dark:border-neutral-700 dark:bg-neutral-900"
                  value={note.position.string}
                  onChange={(e) => updateNote(index, { string: Number(e.target.value) })}
                  title="String (1 = high E, 6 = low E)"
                />
                <input
                  type="number"
                  min={0}
                  max={15}
                  className="w-16 rounded border border-neutral-300 p-1 dark:border-neutral-700 dark:bg-neutral-900"
                  value={note.position.fret}
                  onChange={(e) => updateNote(index, { fret: Number(e.target.value) })}
                  title="Fret"
                />
                <input
                  className="w-20 rounded border border-neutral-300 p-1 dark:border-neutral-700 dark:bg-neutral-900"
                  value={note.pitch}
                  onChange={(e) => updateNote(index, { pitch: e.target.value })}
                  placeholder="Pitch (e.g. G4)"
                />
                <input
                  type="number"
                  className="w-20 rounded border border-neutral-300 p-1 dark:border-neutral-700 dark:bg-neutral-900"
                  value={note.startBeat}
                  onChange={(e) => updateNote(index, { startBeat: Number(e.target.value) })}
                  title="Start beat"
                />
                <input
                  type="number"
                  className="w-24 rounded border border-neutral-300 p-1 dark:border-neutral-700 dark:bg-neutral-900"
                  value={note.durationBeats}
                  onChange={(e) => updateNote(index, { durationBeats: Number(e.target.value) })}
                  title="Duration (beats)"
                />
                <button
                  type="button"
                  className="text-sm text-red-500"
                  onClick={() => setNotes((prev) => prev.filter((_, i) => i !== index))}
                  disabled={notes.length === 1}
                >
                  Remove
                </button>
              </div>
            ))}
          </div>
          <button
            type="button"
            className="mt-2 text-sm text-purple-500 hover:underline"
            onClick={() => setNotes((prev) => [...prev, emptyNote()])}
          >
            + Add note
          </button>
        </div>

        {submitError && <p className="text-red-500">{submitError}</p>}

        <button
          type="submit"
          disabled={!canSubmit}
          className="rounded bg-purple-600 px-4 py-2 text-white disabled:opacity-50"
        >
          {isEditing ? 'Save Changes' : 'Create Lick'}
        </button>
      </form>
      )}
    </section>
  )
}
