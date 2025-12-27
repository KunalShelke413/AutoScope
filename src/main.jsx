import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import { BrowserRouter } from 'react-router-dom';
import { UploadProvider } from './UploadContext';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <BrowserRouter basename="/AutoScope">
    <UploadProvider>
      <App />
    </UploadProvider>
  </BrowserRouter>
);
