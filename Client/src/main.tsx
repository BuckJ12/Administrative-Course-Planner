import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { ModalContext } from './Shared/components/ModalContext.jsx';
import './index.css';
import App from './App.tsx';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ModalContext.Provider value={{ undefined }}>
      <App />
    </ModalContext.Provider>
  </StrictMode>
);
