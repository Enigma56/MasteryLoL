import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router'
import './static/output.css'
import App from './App.jsx'
import Profile from './PlayerProfile/Profile.jsx'

const root = document.getElementById('root')

createRoot(root).render(
  <StrictMode>
      <BrowserRouter>
          <Routes>
              <Route index element={<App/>} />
              <Route path="/profile" element={<Profile/>}/>
          </Routes>
      </BrowserRouter>
  </StrictMode>,
)
