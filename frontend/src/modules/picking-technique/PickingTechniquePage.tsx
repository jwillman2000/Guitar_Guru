export function PickingTechniquePage() {
  return (
    <section className="p-6">
      <h1 className="mb-4 text-2xl font-semibold">Picking Technique</h1>
      <p className="text-neutral-500">
        Alternate/economy/sweep picking, string-skipping, hybrid picking, and tremolo, paired
        with a BPM tracker. Built last per the fixed module order. Any metronome logic will use
        Web Audio API look-ahead scheduling, not setInterval/setTimeout.
      </p>
    </section>
  )
}
