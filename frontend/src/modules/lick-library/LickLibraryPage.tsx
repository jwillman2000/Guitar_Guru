import { TabViewer } from '../../components/tab/TabViewer'

export function LickLibraryPage() {
  return (
    <section className="p-6">
      <h1 className="mb-4 text-2xl font-semibold">Lick Library</h1>
      <p className="mb-6 text-neutral-500">
        Hand-curated iconic licks, tagged back to Scale Fluency positions. Built after Scale
        Fluency per the fixed module order.
      </p>
      <TabViewer title="Example lick" />
    </section>
  )
}
