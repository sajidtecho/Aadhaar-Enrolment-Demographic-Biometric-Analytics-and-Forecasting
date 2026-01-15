import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import MainLayout from './components/layout/MainLayout';
import Dashboard from './pages/Dashboard';
import Prediction from './pages/Prediction';
import AnomalyDetection from './pages/AnomalyDetection';
import ModelInsights from './pages/ModelInsights';

import ModelVerification from './pages/ModelVerification';

// Placeholder Pages (will be replaced later)
const About = () => <div>About Page Content</div>;

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainLayout />}>
          <Route index element={<Dashboard />} />
          <Route path="predict/:type" element={<Prediction />} />
          <Route path="anomalies" element={<AnomalyDetection />} />
          <Route path="insights" element={<ModelInsights />} />
          <Route path="verify" element={<ModelVerification />} />
          <Route path="about" element={<About />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
