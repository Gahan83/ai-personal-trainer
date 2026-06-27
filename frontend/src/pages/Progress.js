import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import { Award, TrendingUp, AlertTriangle, Dumbbell } from 'lucide-react';
import trainerApi from '../services/trainerApi';

const Container = styled.div`max-width: 1000px; margin: 0 auto;`;
const Grid = styled.div`display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;`;
const Stat = styled.div`
  background: white; padding: 1.25rem; border-radius: 1rem; border: 1px solid ${(p) => p.theme.colors.border};
  display: flex; gap: 1rem; align-items: center;
`;
const Icon = styled.div`
  width: 3rem; height: 3rem; border-radius: 50%; background: ${(p) => p.theme.colors.primaryLight};
  color: ${(p) => p.theme.colors.primary}; display: flex; align-items: center; justify-content: center;
`;
const Val = styled.div`font-size: 1.5rem; font-weight: 700; color: ${(p) => p.theme.colors.text.primary};`;
const Lbl = styled.div`font-size: 0.85rem; color: ${(p) => p.theme.colors.text.secondary};`;
const Card = styled.div`background: white; padding: 1.5rem; border-radius: 1rem; border: 1px solid ${(p) => p.theme.colors.border};`;
const Tbl = styled.table`width: 100%; border-collapse: collapse; th, td { text-align: left; padding: 0.6rem 0.5rem; border-bottom: 1px solid ${(p) => p.theme.colors.border}; } th { color: ${(p) => p.theme.colors.text.secondary}; font-size: 0.8rem; }`;
const Tag = styled.span`background: #FEF2F2; color: #B91C1C; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 600;`;

export default function Progress() {
  const [data, setData] = useState(null);
  const [err, setErr] = useState(false);

  useEffect(() => {
    trainerApi.progress().then(setData).catch(() => setErr(true));
  }, []);

  if (err) return <Container><Card>Backend unavailable.</Card></Container>;
  if (!data) return <Container><p>Loading progress…</p></Container>;

  return (
    <Container>
      <h1 style={{ marginBottom: '1.5rem' }}>Progress</h1>
      <Grid>
        <Stat><Icon><Award size={22} /></Icon><div><Val>{data.sessions_completed}</Val><Lbl>Sessions completed</Lbl></div></Stat>
        <Stat><Icon><TrendingUp size={22} /></Icon><div><Val>{data.total_volume_kg.toLocaleString()}</Val><Lbl>Total volume (kg)</Lbl></div></Stat>
        <Stat><Icon><AlertTriangle size={22} /></Icon><div><Val>{data.plateau_alerts.length}</Val><Lbl>Plateau alerts</Lbl></div></Stat>
      </Grid>

      <Card>
        <h2 style={{ fontSize: '1.1rem', marginBottom: '1rem' }}>Per-exercise trends</h2>
        {data.exercises.length === 0 ? (
          <p style={{ color: '#64748B', display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
            <Dumbbell size={18} /> No sets logged yet. Log sets on the Today page to see PRs & volume.
          </p>
        ) : (
          <Tbl>
            <thead>
              <tr><th>Exercise</th><th>PR (kg)</th><th>Volume (kg)</th><th>Sets</th><th>Status</th></tr>
            </thead>
            <tbody>
              {data.exercises.map((e) => (
                <tr key={e.exercise}>
                  <td>{e.exercise}</td>
                  <td>{e.pr_weight_kg ?? '—'}</td>
                  <td>{e.total_volume_kg.toLocaleString()}</td>
                  <td>{e.sets_logged}</td>
                  <td>{e.plateau ? <Tag>Plateau</Tag> : '↗ progressing'}</td>
                </tr>
              ))}
            </tbody>
          </Tbl>
        )}
      </Card>
    </Container>
  );
}
