import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { apiGet } from '../../lib/api'
import type { CanonicalLick } from '../../types/exercise'

export function LickLibraryPage() {
  const [licks, setLicks] = useState<CanonicalLick[] | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    apiGet<CanonicalLick[]>('/api/v1/licks/')
      .then(setLicks)
      .catch((err: Error) => setError(err.message))
  }, [])

  return (
    <section className="p-6">
      <div className="mb-4 flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Lick Library</h1>
        <Link to="/lick-library/new" className="rounded bg-purple-600 px-3 py-1.5 text-sm text-white">
          + Add Lick
        </Link>
      </div>
      <p className="mb-6 text-neutral-500">
        Hand-curated iconic licks, tagged back to Scale Fluency positions.
      </p>

      {error && <p className="text-red-500">Failed to load licks: {error}</p>}
      {!error && licks === null && <p className="text-neutral-500">Loading…</p>}
      {licks !== null && licks.length === 0 && (
        <p className="text-neutral-500">
          No licks yet — this library starts empty and grows one hand-curated entry at a time.
        </p>
      )}

      {licks !== null && licks.length > 0 && (
        <ul className="space-y-3">
          {licks.map((lick) => (
            <li key={lick.id}>
              <Link
                to={`/lick-library/${lick.id}`}
                className="block rounded border border-neutral-300 p-4 hover:border-purple-500 dark:border-neutral-700"
              >
                <div className="font-medium">{lick.title}</div>
                <div className="text-sm text-neutral-500">
                  {lick.song}
                  {lick.artist ? ` — ${lick.artist}` : ''}
                </div>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}
