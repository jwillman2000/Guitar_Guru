import { NavLink } from 'react-router-dom'

const MODULES = [
  { path: '/fretboard-literacy', label: 'Fretboard Literacy' },
  { path: '/scale-fluency', label: 'Scale Fluency' },
  { path: '/lick-library', label: 'Lick Library' },
  { path: '/picking-technique', label: 'Picking Technique' },
]

export function NavBar() {
  return (
    <nav className="flex flex-wrap gap-4 border-b border-neutral-200 p-4 dark:border-neutral-800">
      {MODULES.map((m) => (
        <NavLink
          key={m.path}
          to={m.path}
          className={({ isActive }) =>
            isActive
              ? 'font-semibold text-purple-600 dark:text-purple-400'
              : 'text-neutral-600 dark:text-neutral-400'
          }
        >
          {m.label}
        </NavLink>
      ))}
    </nav>
  )
}
