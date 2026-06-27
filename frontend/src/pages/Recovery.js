import React, { useEffect, useState, useCallback } from 'react';
import styled from 'styled-components';
import toast from 'react-hot-toast';
import { HeartPulse, Moon, Activity, Footprints } from 'lucide-react';
import trainerApi from '../services/trainerApi';

const Container = styled.div`max-width: 800px; margin: 0 auto;`;
const Card = styled.div`background: white; padding: 1.5rem; border-radius: 1rem; border: 1px solid ${(p) => p.theme.colors.border}; margin-bottom: 1.5rem;`;
const Score = styled.div`
  font-size: 3rem; font-weight: 700;
  color: ${(p) => (p.$s >= 75 ? p.theme.colors.success : p.$s >= 50 ? p.theme.colors.warning : p.theme.colors.error)};
`;
const Advice = styled.div`background: ${(p) => p.theme.colors.primaryLight}; color: ${(p) => p.theme.colors.primaryDark}; padding: 0.9rem 1.1rem; border-radius: 0.6rem; margin-top: 0.5rem;`;
const Grid = styled.div`display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.75rem; margin-top: 1rem;`;
const Field = styled.label`display: flex; flex-direction: column; gap: 0.3rem; font-size: 0.85rem; color: ${(p) => p.theme.colors.text.secondary};`;
const Input = styled.input`padding: 0.6rem; border: 1px solid ${(p) => p.theme.colors.border}; border-radius: 0.5rem;`;
const Button = styled.button`margin-top: 1rem; background: ${(p) => p.theme.colors.primary}; color: white; border: none; padding: 0.6rem 1.1rem; border-radius: 0.5rem; font-weight: 600; cursor: pointer;`;
const Metric = styled.div`display: flex; gap: 0.5rem; align-items: center; color: ${(p) => p.theme.colors.text.secondary}; font-size: 0.9rem;`;

export default function Recovery() {
  const [data, setData] = useState(null);
  const [form, setForm] = useState({ sleep_hours: '', hrv_ms: '', resting_hr: '', steps: '' });

  const load = useCallback(() => trainerApi.getWearable().then(setData).catch(() => toast.error('Backend unavailable')), []);
  useEffect(() => { load(); }, [load]);

  const sync = async () => {
    const body = { source: 'manual' };
    Object.entries(form).forEach(([k, v]) => { if (v !== '') body[k] = parseFloat(v); });
    await trainerApi.syncWearable(body);
    toast.success('Synced — recovery updated');
    setForm({ sleep_hours: '', hrv_ms: '', resting_hr: '', steps: '' });
    load();
  };

  if (!data) return <Container><p>Loading…</p></Container>;
  const rec = data.recovery;
  const w = data.data;

  return (
    <Container>
      <h1 style={{ marginBottom: '1.5rem' }}>Recovery</h1>
      <Card>
        <h2 style={{ fontSize: '1.1rem', marginBottom: '0.5rem' }}><HeartPulse size={18} style={{ verticalAlign: -3 }} /> Recovery score</h2>
        <Score $s={rec.score ?? 0}>{rec.score ?? '—'}</Score>
        <Advice>{rec.advice}</Advice>
        {w && (
          <Grid>
            <Metric><Moon size={16} /> Sleep: {w.sleep_hours ?? '—'} h</Metric>
            <Metric><Activity size={16} /> HRV: {w.hrv_ms ?? '—'} ms</Metric>
            <Metric><HeartPulse size={16} /> Resting HR: {w.resting_hr ?? '—'}</Metric>
            <Metric><Footprints size={16} /> Steps: {w.steps ?? '—'}</Metric>
          </Grid>
        )}
      </Card>

      <Card>
        <h2 style={{ fontSize: '1.1rem', marginBottom: '0.5rem' }}>Log health data</h2>
        <p style={{ color: '#64748B', fontSize: '0.85rem' }}>
          Apple Health / Google Fit / Fitbit sync is a V3 integration — enter manually for now.
        </p>
        <Grid>
          <Field>Sleep (hours)<Input value={form.sleep_hours} onChange={(e) => setForm({ ...form, sleep_hours: e.target.value })} /></Field>
          <Field>HRV (ms)<Input value={form.hrv_ms} onChange={(e) => setForm({ ...form, hrv_ms: e.target.value })} /></Field>
          <Field>Resting HR<Input value={form.resting_hr} onChange={(e) => setForm({ ...form, resting_hr: e.target.value })} /></Field>
          <Field>Steps<Input value={form.steps} onChange={(e) => setForm({ ...form, steps: e.target.value })} /></Field>
        </Grid>
        <Button onClick={sync}>Sync</Button>
      </Card>
    </Container>
  );
}
