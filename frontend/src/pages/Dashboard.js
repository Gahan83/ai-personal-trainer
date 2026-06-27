import React, { useEffect, useState, useCallback } from 'react';
import styled from 'styled-components';
import toast from 'react-hot-toast';
import { CheckCircle, SkipForward, Plus, Sparkles } from 'lucide-react';
import trainerApi from '../services/trainerApi';

const Container = styled.div`max-width: 1000px; margin: 0 auto;`;
const Card = styled.div`
  background: white; padding: 1.5rem; border-radius: 1rem;
  box-shadow: ${(p) => p.theme.shadows.sm}; margin-bottom: 1.5rem;
  border: 1px solid ${(p) => p.theme.colors.border};
`;
const Row = styled.div`display: flex; gap: 1rem; align-items: center; flex-wrap: wrap;`;
const Title = styled.h2`font-size: 1.25rem; margin-bottom: 0.75rem; color: ${(p) => p.theme.colors.text.primary};`;
const Muted = styled.p`color: ${(p) => p.theme.colors.text.secondary}; font-size: 0.9rem;`;

const WeekGrid = styled.div`display: grid; grid-template-columns: repeat(7, 1fr); gap: 0.5rem;`;
const Day = styled.div`
  border-radius: 0.5rem; padding: 0.6rem 0.3rem; text-align: center;
  font-size: 0.75rem; border: 1px solid ${(p) => p.theme.colors.border};
  background: ${(p) => (p.$today ? p.theme.colors.primaryLight : p.$training ? '#F1F5F9' : 'white')};
  outline: ${(p) => (p.$today ? `2px solid ${p.theme.colors.primary}` : 'none')};
`;
const DayName = styled.div`font-weight: 600; color: ${(p) => p.theme.colors.text.secondary}; margin-bottom: 4px;`;
const DayType = styled.div`color: ${(p) => p.theme.colors.text.primary}; text-transform: capitalize; font-weight: 500;`;

const Badge = styled.span`
  display: inline-block; font-size: 0.7rem; font-weight: 600; padding: 3px 10px;
  border-radius: 20px; background: ${(p) => p.theme.colors.primaryLight}; color: ${(p) => p.theme.colors.primary};
`;
const Pill = styled.button`
  border: 1px solid ${(p) => p.theme.colors.border}; cursor: pointer;
  padding: 0.4rem 0.8rem; border-radius: 20px; font-size: 0.85rem; font-weight: 600;
  color: ${(p) => (p.$active ? 'white' : p.theme.colors.text.secondary)};
  background: ${(p) => (p.$active ? p.theme.colors.primary : 'white')};
`;
const Button = styled.button`
  background: ${(p) => (p.$secondary ? 'white' : p.theme.colors.primary)};
  color: ${(p) => (p.$secondary ? p.theme.colors.text.secondary : 'white')};
  border: 1px solid ${(p) => (p.$secondary ? p.theme.colors.border : p.theme.colors.primary)};
  padding: 0.6rem 1.1rem; border-radius: 0.5rem; font-weight: 600; cursor: pointer;
  display: inline-flex; align-items: center; gap: 0.4rem;
  &:disabled { opacity: 0.5; cursor: not-allowed; }
`;
const Input = styled.input`
  padding: 0.5rem; border: 1px solid ${(p) => p.theme.colors.border}; border-radius: 0.4rem;
  width: 90px; font-size: 0.9rem;
`;
const Exercise = styled.div`
  padding: 0.9rem 0; border-bottom: 1px solid ${(p) => p.theme.colors.border};
  &:last-child { border-bottom: none; }
`;
const ExName = styled.div`font-weight: 600; color: ${(p) => p.theme.colors.text.primary};`;
const Note = styled.div`
  background: #FFFBEB; border: 1px solid #FDE68A; color: #92400E;
  padding: 0.6rem 0.9rem; border-radius: 0.5rem; font-size: 0.85rem; margin-top: 0.5rem;
`;
const CoachNote = styled.div`
  background: ${(p) => p.theme.colors.primaryLight}; color: ${(p) => p.theme.colors.primaryDark};
  padding: 0.9rem 1.1rem; border-radius: 0.6rem; margin-bottom: 1rem; display: flex; gap: 0.6rem;
`;

const SCALE = [1, 2, 3, 4, 5];

function CheckinForm({ onSubmit }) {
  const [soreness, setSoreness] = useState(2);
  const [energy, setEnergy] = useState(3);
  const [muscles, setMuscles] = useState([]);
  const toggle = (m) => setMuscles((x) => (x.includes(m) ? x.filter((y) => y !== m) : [...x, m]));
  const groups = ['legs', 'chest', 'back', 'shoulders', 'arms'];
  return (
    <Card>
      <Title>30-second readiness check-in</Title>
      <Muted>How sore are you? (1 none → 5 very sore)</Muted>
      <Row style={{ margin: '0.5rem 0 1rem' }}>
        {SCALE.map((n) => (
          <Pill key={n} $active={soreness === n} onClick={() => setSoreness(n)}>{n}</Pill>
        ))}
      </Row>
      <Muted>Energy level? (1 drained → 5 great)</Muted>
      <Row style={{ margin: '0.5rem 0 1rem' }}>
        {SCALE.map((n) => (
          <Pill key={n} $active={energy === n} onClick={() => setEnergy(n)}>{n}</Pill>
        ))}
      </Row>
      <Muted>Any sore muscles?</Muted>
      <Row style={{ margin: '0.5rem 0 1rem' }}>
        {groups.map((m) => (
          <Pill key={m} $active={muscles.includes(m)} onClick={() => toggle(m)} style={{ textTransform: 'capitalize' }}>{m}</Pill>
        ))}
      </Row>
      <Button onClick={() => onSubmit({ soreness, energy, sore_muscles: muscles })}>Submit check-in</Button>
    </Card>
  );
}

function ExerciseRow({ ex, onLog }) {
  const [reps, setReps] = useState('');
  const [weight, setWeight] = useState('');
  return (
    <Exercise>
      <Row style={{ justifyContent: 'space-between' }}>
        <div>
          <ExName>{ex.name}</ExName>
          <Muted>{ex.sets} × {ex.reps} · rest {ex.rest}s{ex.cue ? ` · ${ex.cue}` : ''}</Muted>
        </div>
        <Row>
          <Input placeholder="reps" value={reps} onChange={(e) => setReps(e.target.value)} />
          <Input placeholder="kg" value={weight} onChange={(e) => setWeight(e.target.value)} />
          <Button $secondary onClick={() => { onLog(ex.name, reps, weight); setReps(''); setWeight(''); }}>
            <Plus size={16} /> Log
          </Button>
        </Row>
      </Row>
    </Exercise>
  );
}

export default function Dashboard() {
  const [week, setWeek] = useState(null);
  const [today, setToday] = useState(null);
  const [checkin, setCheckin] = useState(null);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    try {
      const [w, t, c] = await Promise.all([
        trainerApi.getWeek(),
        trainerApi.getToday(),
        trainerApi.getTodayCheckin(),
      ]);
      setWeek(w); setToday(t); setCheckin(c);
    } catch (e) {
      toast.error('Could not reach backend. Is it running on :8000?');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const submitCheckin = async (body) => {
    await trainerApi.submitCheckin(body);
    toast.success('Check-in saved — plan adapted.');
    await load();
  };
  const logSet = async (exercise, reps, weight) => {
    if (!today?.session_id) return;
    try {
      await trainerApi.logSet(today.session_id, {
        exercise,
        reps: reps ? parseInt(reps, 10) : null,
        weight_kg: weight ? parseFloat(weight) : null,
      });
      toast.success(`Logged ${exercise}`);
    } catch (e) {
      toast.error(e.response?.data?.detail || 'Could not log set');
    }
  };
  const complete = async () => {
    await trainerApi.completeSession(today.session_id, {});
    toast.success('Session completed! 💪');
    await load();
  };
  const skip = async () => {
    await trainerApi.skipSession(today.session_id);
    toast('Session skipped — agent will reshuffle.');
    await load();
  };

  if (loading) return <Container><p>Loading your day…</p></Container>;
  if (!today) return <Container><Card>Backend unavailable.</Card></Container>;

  const plan = today.plan;
  const isTraining = plan?.is_training;

  return (
    <Container>
      <h1 style={{ marginBottom: '0.25rem' }}>Hi Gahan 👋</h1>
      <Muted style={{ marginBottom: '1.5rem' }}>{today.date} · today is <b>{plan.title}</b></Muted>

      {!today.ai_enabled && (
        <Note style={{ marginBottom: '1.5rem' }}>
          AI chat & coaching notes are off. Add your Azure OpenAI keys in <code>backend/.env</code> to enable.
        </Note>
      )}

      {week && (
        <Card>
          <Title>This week</Title>
          <WeekGrid>
            {week.overview.map((d) => (
              <Day key={d.day} $training={d.is_training} $today={d.title === plan.title}>
                <DayName>{d.day}</DayName>
                <DayType>{d.day_type}</DayType>
              </Day>
            ))}
          </WeekGrid>
          {week.violations?.length > 0 && (
            <Note>Constraint issues: {week.violations.join(' ')}</Note>
          )}
        </Card>
      )}

      {!checkin && <CheckinForm onSubmit={submitCheckin} />}

      {today.adapted && (
        <Note style={{ marginBottom: '1.5rem' }}>
          Plan adapted: {today.adaptation_reason} (was {today.planned_day_type} day)
        </Note>
      )}

      <Card>
        <Row style={{ justifyContent: 'space-between' }}>
          <Title style={{ margin: 0 }}>{plan.title}</Title>
          <Badge>{plan.estimated_minutes} min</Badge>
        </Row>

        {today.coach_note && (
          <CoachNote><Sparkles size={18} /> <span>{today.coach_note}</span></CoachNote>
        )}

        {plan.notes?.map((n, i) => <Note key={i}>{n}</Note>)}

        {isTraining ? (
          <>
            <div style={{ marginTop: '1rem' }}>
              {plan.exercises.map((ex, i) => (
                <ExerciseRow key={i} ex={ex} onLog={logSet} />
              ))}
            </div>
            <Row style={{ marginTop: '1.25rem' }}>
              <Button onClick={complete} disabled={today.status === 'completed'}>
                <CheckCircle size={18} /> {today.status === 'completed' ? 'Completed' : 'Mark complete'}
              </Button>
              <Button $secondary onClick={skip}><SkipForward size={18} /> Skip</Button>
            </Row>
          </>
        ) : (
          <Muted style={{ marginTop: '1rem' }}>Rest day — recover, hydrate, sleep well. No training scheduled.</Muted>
        )}
      </Card>
    </Container>
  );
}
