import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router'
import './static/output.css'
import App from './App.jsx'

const root = document.getElementById('root')

createRoot(root).render(
  <StrictMode>
      <BrowserRouter>
          {/*<App />*/}
          <Routes>
              <Route index element={<App/>} />
          </Routes>
      </BrowserRouter>
  </StrictMode>,
)
