import React, { useEffect, useState, useCallback } from 'react';
import styled from 'styled-components';
import toast from 'react-hot-toast';
import { Droplet, Beef } from 'lucide-react';
import trainerApi from '../services/trainerApi';

const Container = styled.div`max-width: 800px; margin: 0 auto;`;
const Card = styled.div`background: white; padding: 1.5rem; border-radius: 1rem; border: 1px solid ${(p) => p.theme.colors.border}; margin-bottom: 1.5rem;`;
const Guidance = styled.div`background: ${(p) => p.theme.colors.primaryLight}; color: ${(p) => p.theme.colors.primaryDark}; padding: 1rem; border-radius: 0.6rem; line-height: 1.5;`;
const Bar = styled.div`height: 12px; background: ${(p) => p.theme.colors.border}; border-radius: 6px; overflow: hidden; margin: 0.5rem 0;`;
const Fill = styled.div`height: 100%; width: ${(p) => p.$pct}%; background: ${(p) => p.theme.colors.success};`;
const Row = styled.div`display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap;`;
const Input = styled.input`padding: 0.6rem; border: 1px solid ${(p) => p.theme.colors.border}; border-radius: 0.5rem; width: 120px;`;
const Button = styled.button`background: ${(p) => p.theme.colors.primary}; color: white; border: none; padding: 0.6rem 1.1rem; border-radius: 0.5rem; font-weight: 600; cursor: pointer;`;
const Hydrate = styled.div`background: #ECFEFF; border: 1px solid #A5F3FC; color: #155E75; padding: 0.8rem 1rem; border-radius: 0.6rem; display: flex; gap: 0.5rem; margin-top: 1rem;`;

export default function Nutrition() {
  const [data, setData] = useState(null);
  const [protein, setProtein] = useState('');
  const [water, setWater] = useState('');

  const load = useCallback(() => trainerApi.getNudges().then(setData).catch(() => toast.error('Backend unavailable')), []);
  useEffect(() => { load(); }, [load]);

  const log = async () => {
    await trainerApi.logNutrition({
      protein_g: protein ? parseFloat(protein) : null,
      water_ml: water ? parseFloat(water) : null,
    });
    toast.success('Logged');
    setProtein(''); setWater('');
    load();
  };

  if (!data) return <Container><p>Loading…</p></Container>;
  const pct = data.protein_target_g ? Math.min(100, (data.protein_logged_g / data.protein_target_g) * 100) : 0;

  return (
    <Container>
      <h1 style={{ marginBottom: '1.5rem' }}>Nutrition & Hydration</h1>
      <Card>
        <h2 style={{ fontSize: '1.1rem', marginBottom: '0.75rem', textTransform: 'capitalize' }}>{data.day_type} day guidance</h2>
        <Guidance>{data.guidance}</Guidance>
        {data.hydrate_extra && <Hydrate><Droplet size={18} /> Football today — hydrate extra: 500ml before, sip every break.</Hydrate>}
      </Card>

      <Card>
        <h2 style={{ fontSize: '1.1rem', marginBottom: '0.75rem' }}><Beef size={18} style={{ verticalAlign: -3 }} /> Protein target</h2>
        <p style={{ color: '#64748B' }}>{data.protein_logged_g}g / {data.protein_target_g}g · {data.protein_remaining_g}g to go</p>
        <Bar><Fill $pct={pct} /></Bar>
        <Row style={{ marginTop: '1rem' }}>
          <Input placeholder="protein g" value={protein} onChange={(e) => setProtein(e.target.value)} />
          <Input placeholder="water ml" value={water} onChange={(e) => setWater(e.target.value)} />
          <Button onClick={log}>Log</Button>
        </Row>
      </Card>
    </Container>
  );
}
