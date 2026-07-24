import { useEffect } from 'react';
import { Routes, Route, useNavigate, useLocation, Navigate } from 'react-router-dom';
import { Layout } from './components/layout/Layout';
import { Dashboard } from './pages/Dashboard';
import { SetupWizard } from './pages/SetupWizard';
import { NewProject } from './pages/NewProject';
import { ProjectDetail } from './pages/ProjectDetail';
import { ClipMode } from './pages/ClipMode';
import { Settings } from './pages/Settings';

function App() {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const isSetupComplete = localStorage.getItem('setup_complete');
    if (!isSetupComplete && location.pathname !== '/setup') {
      navigate('/setup');
    }
  }, [navigate, location]);

  return (
    <Routes>
      <Route path="/setup" element={<SetupWizard />} />
      <Route
        path="/*"
        element={
          <Layout>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/new" element={<NewProject />} />
              <Route path="/project/:id" element={<ProjectDetail />} />
              <Route path="/clip" element={<ClipMode />} />
              <Route path="/settings" element={<Settings />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </Layout>
        }
      />
    </Routes>
  );
}

export default App;
