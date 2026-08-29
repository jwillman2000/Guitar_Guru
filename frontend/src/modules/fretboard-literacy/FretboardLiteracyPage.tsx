import { Fretboard } from '../../components/fretboard/Fretboard'

export function FretboardLiteracyPage() {
  return (
    <section className="p-6">
      <h1 className="mb-4 text-2xl font-semibold">Fretboard Literacy</h1>
      <p className="mb-6 text-neutral-500">
        Note-identity drills across the fretboard. Exercise generation lands in Phase 3.
      </p>
      <Fretboard />
    </section>
  )
}
