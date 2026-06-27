import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import toast from 'react-hot-toast';
import { User } from 'lucide-react';
import trainerApi from '../services/trainerApi';

const Container = styled.div`max-width: 700px; margin: 0 auto;`;
const Card = styled.div`background: white; padding: 2rem; border-radius: 1rem; border: 1px solid ${(p) => p.theme.colors.border};`;
const Head = styled.div`display: flex; align-items: center; gap: 1.5rem; margin-bottom: 2rem;`;
const Avatar = styled.div`width: 4.5rem; height: 4.5rem; border-radius: 50%; background: ${(p) => p.theme.colors.primaryLight}; color: ${(p) => p.theme.colors.primary}; display: flex; align-items: center; justify-content: center;`;
const Form = styled.div`display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem;`;
const Field = styled.label`display: flex; flex-direction: column; gap: 0.4rem; font-weight: 600; color: ${(p) => p.theme.colors.text.primary}; font-size: 0.9rem;`;
const Input = styled.input`padding: 0.7rem; border: 1px solid ${(p) => p.theme.colors.border}; border-radius: 0.5rem; font-weight: 400; &:focus { outline: none; border-color: ${(p) => p.theme.colors.primary}; }`;
const Button = styled.button`margin-top: 1.5rem; background: ${(p) => p.theme.colors.primary}; color: white; border: none; padding: 0.7rem 1.4rem; border-radius: 0.5rem; font-weight: 600; cursor: pointer;`;
const Pill = styled.span`display: inline-block; padding: 4px 12px; border-radius: 20px; background: ${(p) => p.theme.colors.primaryLight}; color: ${(p) => p.theme.colors.primary}; font-size: 0.8rem; font-weight: 600; margin: 0 4px 4px 0; text-transform: capitalize;`;

export default function Profile() {
  const [p, setP] = useState(null);

  useEffect(() => { trainerApi.getProfile().then(setP).catch(() => toast.error('Backend unavailable')); }, []);

  const save = async () => {
    const body = {
      full_name: p.full_name,
      age: p.age ? parseInt(p.age, 10) : null,
      height_cm: p.height_cm ? parseFloat(p.height_cm) : null,
      weight_kg: p.weight_kg ? parseFloat(p.weight_kg) : null,
      goals: p.goals,
      experience_level: p.experience_level,
      protein_target_g: p.protein_target_g ? parseInt(p.protein_target_g, 10) : null,
    };
    const updated = await trainerApi.updateProfile(body);
    setP(updated);
    toast.success('Profile updated');
  };

  if (!p) return <Container><p>Loading…</p></Container>;
  const set = (k) => (e) => setP({ ...p, [k]: e.target.value });

  return (
    <Container>
      <h1 style={{ marginBottom: '1.5rem' }}>Profile</h1>
      <Card>
        <Head>
          <Avatar><User size={32} /></Avatar>
          <div>
            <h2 style={{ fontSize: '1.4rem' }}>{p.full_name}</h2>
            <p style={{ color: '#64748B' }}>{p.email} · {p.location}</p>
          </div>
        </Head>

        <div style={{ marginBottom: '1.5rem' }}>
          {(p.weekly_split || []).map((d, i) => <Pill key={i}>{d}</Pill>)}
        </div>

        <Form>
          <Field>Full name<Input value={p.full_name || ''} onChange={set('full_name')} /></Field>
          <Field>Experience<Input value={p.experience_level || ''} onChange={set('experience_level')} /></Field>
          <Field>Age<Input value={p.age || ''} onChange={set('age')} /></Field>
          <Field>Height (cm)<Input value={p.height_cm || ''} onChange={set('height_cm')} /></Field>
          <Field>Weight (kg)<Input value={p.weight_kg || ''} onChange={set('weight_kg')} /></Field>
          <Field>Protein target (g)<Input value={p.protein_target_g || ''} onChange={set('protein_target_g')} /></Field>
          <Field style={{ gridColumn: '1 / -1' }}>Goals<Input value={p.goals || ''} onChange={set('goals')} /></Field>
        </Form>
        <Button onClick={save}>Save changes</Button>
      </Card>
    </Container>
  );
}
