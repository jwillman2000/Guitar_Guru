// Placeholder for the AlphaTab integration (Phase 4 — Visualization).
// AlphaTab itself isn't installed yet; this establishes where tab/playback
// rendering will live once that phase starts.

interface TabViewerProps {
  title: string
}

export function TabViewer({ title }: TabViewerProps) {
  return (
    <div className="rounded border border-dashed border-neutral-400 p-6 text-center text-sm text-neutral-500 dark:border-neutral-600">
      Tab viewer for "{title}" — AlphaTab integration pending (Phase 4)
    </div>
  )
}
