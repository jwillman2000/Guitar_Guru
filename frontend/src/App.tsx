import { Navigate, Route, Routes } from 'react-router-dom'
import { NavBar } from './components/layout/NavBar'
import { FretboardLiteracyPage } from './modules/fretboard-literacy/FretboardLiteracyPage'
import { LickLibraryPage } from './modules/lick-library/LickLibraryPage'
import { PickingTechniquePage } from './modules/picking-technique/PickingTechniquePage'
import { ScaleFluencyPage } from './modules/scale-fluency/ScaleFluencyPage'

function App() {
  return (
    <div className="min-h-screen bg-white text-neutral-900 dark:bg-neutral-950 dark:text-neutral-100">
      <NavBar />
      <Routes>
        <Route path="/" element={<Navigate to="/fretboard-literacy" replace />} />
        <Route path="/fretboard-literacy" element={<FretboardLiteracyPage />} />
        <Route path="/scale-fluency" element={<ScaleFluencyPage />} />
        <Route path="/lick-library" element={<LickLibraryPage />} />
        <Route path="/picking-technique" element={<PickingTechniquePage />} />
      </Routes>
    </div>
  )
}

export default App
