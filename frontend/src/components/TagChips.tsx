interface TagChipsProps {
  genreTags: string[]
  techniqueTags: string[]
}

export function TagChips({ genreTags, techniqueTags }: TagChipsProps) {
  if (genreTags.length === 0 && techniqueTags.length === 0) return null
  return (
    <div className="mb-4 flex flex-wrap gap-2 text-sm">
      {genreTags.map((tag) => (
        <span key={tag} className="rounded-full bg-purple-100 px-2 py-0.5 dark:bg-purple-900">
          {tag}
        </span>
      ))}
      {techniqueTags.map((tag) => (
        <span key={tag} className="rounded-full bg-neutral-200 px-2 py-0.5 dark:bg-neutral-800">
          {tag}
        </span>
      ))}
    </div>
  )
}
