import './static/output.css'

import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router'

import Home from './components/Home.jsx'
import Profile from './components/PlayerProfile/Profile.jsx'

const root = document.getElementById('root')
createRoot(root).render(
  <StrictMode>
      <BrowserRouter>
          <Routes>
              <Route index element={<Home/>} />
              <Route path="/profile" element={<Profile/>}/>
          </Routes>
      </BrowserRouter>
  </StrictMode>,
)
