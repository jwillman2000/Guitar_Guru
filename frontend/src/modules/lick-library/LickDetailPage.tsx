import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { TabViewer } from '../../components/tab/TabViewer'
import { apiGet } from '../../lib/api'
import type { CanonicalLick } from '../../types/exercise'

export function LickDetailPage() {
  const { id } = useParams<{ id: string }>()
  const [lick, setLick] = useState<CanonicalLick | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    setLick(null)
    setError(null)
    apiGet<CanonicalLick>(`/api/v1/licks/${id}`)
      .then(setLick)
      .catch((err: Error) => setError(err.message))
  }, [id])

  return (
    <section className="p-6">
      <Link to="/lick-library" className="mb-4 inline-block text-sm text-purple-500 hover:underline">
        ← Back to Lick Library
      </Link>

      {error && <p className="text-red-500">Failed to load lick: {error}</p>}
      {!error && lick === null && <p className="text-neutral-500">Loading…</p>}

      {lick && (
        <>
          <h1 className="mb-1 text-2xl font-semibold">{lick.title}</h1>
          <p className="mb-4 text-neutral-500">
            {lick.song}
            {lick.artist ? ` — ${lick.artist}` : ''} · Key: {lick.key} · Difficulty: {lick.difficulty}
          </p>

          {lick.description && <p className="mb-4">{lick.description}</p>}

          <div className="mb-4 flex flex-wrap gap-2 text-sm">
            {lick.genreTags.map((tag) => (
              <span key={tag} className="rounded-full bg-purple-100 px-2 py-0.5 dark:bg-purple-900">
                {tag}
              </span>
            ))}
            {lick.techniqueTags.map((tag) => (
              <span key={tag} className="rounded-full bg-neutral-200 px-2 py-0.5 dark:bg-neutral-800">
                {tag}
              </span>
            ))}
          </div>

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
