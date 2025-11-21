import { Routes, Route, useLocation } from 'react-router-dom';
import { useEffect } from 'react';
import Nav from './components/nav.jsx';
import Detail from './components/detail.jsx';
import Upload from './components/upload.jsx';
import Dashboard from './components/dashboard.jsx';
import './app.css';

const App = () => {
  const location = useLocation();
  const isDashboard = location.pathname === '/dashboard';

  useEffect(() => {
    if (isDashboard) {
      document.body.style.margin = '0';
      document.body.style.padding = '0';
    } else {
      document.body.style.margin = '';
      document.body.style.padding = '';
    }
  }, [isDashboard]);

  return (
    <div>
      <Routes>
        <Route
          path="/"
          element={
            <div>
              <Nav />
              <div className="container">
                <div className="hero">
                  <Detail />
                  <div className="upload">
                    <h2>Upload Your Code</h2>
                    <Upload />
                  </div>
                </div>
              </div>
            </div>
          }
        />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </div>
  );
};

export default App;
