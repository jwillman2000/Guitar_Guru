import { AlphaTabApi } from '@coderline/alphatab'
import { useEffect, useRef } from 'react'
import { notesToAlphaTex } from '../../lib/alphaTex'
import type { NoteEvent } from '../../types/exercise'

interface TabViewerProps {
  title: string
  notes: NoteEvent[]
}

// Visual notation only — the player/soundfont stays disabled (default), so
// this never produces audio. Playback would be a distinct feature from the
// drill-scoped BPM metronome already built for Picking Technique.
export function TabViewer({ title, notes }: TabViewerProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const apiRef = useRef<AlphaTabApi | null>(null)

  useEffect(() => {
    if (!containerRef.current) return
    // AlphaTab auto-detects its font/worker script locations from its own
    // script file's URL, which isn't reliable under Vite's dev-mode module
    // serving (works fine in a production build, where the vite plugin
    // copies these assets next to the real bundle). Setting fontDirectory
    // explicitly to the app-root-relative path the plugin always copies to
    // sidesteps that auto-detection in both dev and prod.
    const api = new AlphaTabApi(containerRef.current, {
      core: { fontDirectory: '/font/' },
    })
    apiRef.current = api
    return () => {
      api.destroy()
      apiRef.current = null
    }
  }, [])

  useEffect(() => {
    apiRef.current?.tex(notesToAlphaTex(title, notes))
  }, [title, notes])

  return <div ref={containerRef} />
}
