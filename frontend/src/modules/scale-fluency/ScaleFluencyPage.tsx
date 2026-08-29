import { Fretboard } from '../../components/fretboard/Fretboard'

export function ScaleFluencyPage() {
  return (
    <section className="p-6">
      <h1 className="mb-4 text-2xl font-semibold">Scale Fluency</h1>
      <p className="mb-6 text-neutral-500">
        Position-crossing exercises beyond CAGED-box thinking. Built after Fretboard Literacy per
        the fixed module order.
      </p>
      <Fretboard />
    </section>
  )
}
