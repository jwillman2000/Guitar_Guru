import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { TabViewer } from '../../components/tab/TabViewer'
import { TagChips } from '../../components/TagChips'
import { apiDelete, apiGet } from '../../lib/api'
import type { CanonicalLick } from '../../types/exercise'

export function LickDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [lick, setLick] = useState<CanonicalLick | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    setLick(null)
    setError(null)
    apiGet<CanonicalLick>(`/api/v1/licks/${id}`)
      .then(setLick)
      .catch((err: Error) => setError(err.message))
  }, [id])

  async function handleDelete() {
    if (!window.confirm(`Delete "${lick?.title}"? This can't be undone.`)) return
    try {
      await apiDelete(`/api/v1/licks/${id}`)
      navigate('/lick-library')
    } catch (err) {
      setError((err as Error).message)
    }
  }

  return (
    <section className="p-6">
      <Link to="/lick-library" className="mb-4 inline-block text-sm text-purple-500 hover:underline">
        ← Back to Lick Library
      </Link>

      {error && <p className="text-red-500">Failed to load lick: {error}</p>}
      {!error && lick === null && <p className="text-neutral-500">Loading…</p>}

      {lick && (
        <>
          <div className="mb-1 flex items-center justify-between">
            <h1 className="text-2xl font-semibold">{lick.title}</h1>
            <div className="flex gap-2">
              <Link
                to={`/lick-library/${lick.id}/edit`}
                className="rounded border border-neutral-300 px-3 py-1.5 text-sm dark:border-neutral-700"
              >
                Edit
              </Link>
              <button
                onClick={handleDelete}
                className="rounded border border-red-400 px-3 py-1.5 text-sm text-red-500"
              >
                Delete
              </button>
            </div>
          </div>
          <p className="mb-4 text-neutral-500">
            {lick.song}
            {lick.artist ? ` — ${lick.artist}` : ''} · Key: {lick.key} · Difficulty: {lick.difficulty}
          </p>

          {lick.description && <p className="mb-4">{lick.description}</p>}

          <TagChips genreTags={lick.genreTags} techniqueTags={lick.techniqueTags} />

          {lick.scalePositions.length > 0 && (
            <p className="mb-6 text-sm text-neutral-500">
              Crosses Scale Fluency position(s): {lick.scalePositions.join(', ')}
            </p>
          )}

          <TabViewer title={lick.title} />
        </>
      )}
    </section>
  )
}
