import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { Lock } from 'lucide-react';
import api, { PASSWORD_KEY } from '../services/api';

const Screen = styled.div`
  min-height: 100vh; display: flex; align-items: center; justify-content: center;
  background: ${(p) => p.theme.colors.background};
`;
const Box = styled.form`
  background: white; padding: 2.5rem; border-radius: 1rem; width: 360px;
  border: 1px solid ${(p) => p.theme.colors.border}; box-shadow: ${(p) => p.theme.shadows.md};
  text-align: center;
`;
const Icon = styled.div`
  width: 3.5rem; height: 3.5rem; border-radius: 50%; margin: 0 auto 1rem;
  background: ${(p) => p.theme.colors.primaryLight}; color: ${(p) => p.theme.colors.primary};
  display: flex; align-items: center; justify-content: center;
`;
const Input = styled.input`
  width: 100%; padding: 0.8rem; margin: 1rem 0 0.5rem; border-radius: 0.5rem;
  border: 1px solid ${(p) => p.theme.colors.border}; font-size: 1rem;
  &:focus { outline: none; border-color: ${(p) => p.theme.colors.primary}; }
`;
const Button = styled.button`
  width: 100%; padding: 0.8rem; margin-top: 0.5rem; border: none; border-radius: 0.5rem;
  background: ${(p) => p.theme.colors.primary}; color: white; font-weight: 600; cursor: pointer;
  &:disabled { opacity: 0.6; }
`;
const Err = styled.p`color: ${(p) => p.theme.colors.error}; font-size: 0.85rem; margin-top: 0.5rem;`;

// Probes the backend once: if it answers without a password the gate is open
// (local dev); a 401 means a shared secret is required and we show the form.
export default function AccessGate({ children }) {
  const [status, setStatus] = useState('checking'); // checking | need | ok
  const [pw, setPw] = useState('');
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');

  useEffect(() => {
    api.get('/users/profile')
      .then(() => setStatus('ok'))
      .catch((e) => setStatus(e.response?.status === 401 ? 'need' : 'ok'));
  }, []);

  const submit = async (e) => {
    e.preventDefault();
    setBusy(true); setErr('');
    localStorage.setItem(PASSWORD_KEY, pw);
    try {
      await api.get('/users/profile');
      setStatus('ok');
    } catch (e2) {
      localStorage.removeItem(PASSWORD_KEY);
      setErr('Wrong password.');
    } finally {
      setBusy(false);
    }
  };

  if (status === 'checking') return <Screen><p>Loading…</p></Screen>;
  if (status === 'ok') return children;

  return (
    <Screen>
      <Box onSubmit={submit}>
        <Icon><Lock size={26} /></Icon>
        <h2 style={{ fontSize: '1.2rem' }}>AI Personal Trainer</h2>
        <p style={{ color: '#64748B', fontSize: '0.9rem' }}>Enter access password</p>
        <Input type="password" value={pw} onChange={(e) => setPw(e.target.value)} placeholder="Password" autoFocus />
        <Button type="submit" disabled={busy || !pw}>{busy ? 'Checking…' : 'Enter'}</Button>
        {err && <Err>{err}</Err>}
      </Box>
    </Screen>
  );
}
