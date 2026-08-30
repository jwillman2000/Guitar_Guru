// Mirrors backend/app/schemas/tag.py's TagOut.
export interface Tag {
  id: number
  category: 'genre' | 'technique' | 'position'
  name: string
  slug: string
}
