import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { ThemeProvider } from 'styled-components';
import { GlobalStyle, theme } from './styles/theme';
import Layout from './components/Layout';
import AccessGate from './components/AccessGate';
import Dashboard from './pages/Dashboard';
import Coach from './pages/Coach';
import Progress from './pages/Progress';
import Nutrition from './pages/Nutrition';
import Recovery from './pages/Recovery';
import Profile from './pages/Profile';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <GlobalStyle />
      <AccessGate>
        <Layout>
          <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/coach" element={<Coach />} />
          <Route path="/progress" element={<Progress />} />
          <Route path="/nutrition" element={<Nutrition />} />
          <Route path="/recovery" element={<Recovery />} />
          <Route path="/profile" element={<Profile />} />
          </Routes>
        </Layout>
      </AccessGate>
    </ThemeProvider>
  );
}

export default App;
