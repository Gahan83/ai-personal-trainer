import React, { useState, useRef, useEffect } from 'react';
import styled from 'styled-components';
import toast from 'react-hot-toast';
import { Send } from 'lucide-react';
import trainerApi from '../services/trainerApi';

const Container = styled.div`max-width: 800px; margin: 0 auto; display: flex; flex-direction: column; height: calc(100vh - 140px);`;
const Thread = styled.div`flex: 1; overflow-y: auto; padding: 0.5rem; display: flex; flex-direction: column; gap: 0.75rem;`;
const Bubble = styled.div`
  max-width: 75%; padding: 0.75rem 1rem; border-radius: 1rem; line-height: 1.5; white-space: pre-wrap;
  align-self: ${(p) => (p.$me ? 'flex-end' : 'flex-start')};
  background: ${(p) => (p.$me ? p.theme.colors.primary : 'white')};
  color: ${(p) => (p.$me ? 'white' : p.theme.colors.text.primary)};
  border: 1px solid ${(p) => (p.$me ? p.theme.colors.primary : p.theme.colors.border)};
`;
const Composer = styled.form`display: flex; gap: 0.5rem; padding-top: 0.75rem;`;
const Input = styled.input`
  flex: 1; padding: 0.8rem 1rem; border: 1px solid ${(p) => p.theme.colors.border};
  border-radius: 0.6rem; font-size: 1rem;
  &:focus { outline: none; border-color: ${(p) => p.theme.colors.primary}; }
`;
const SendButton = styled.button`
  background: ${(p) => p.theme.colors.primary}; color: white; border: none;
  border-radius: 0.6rem; padding: 0 1.1rem; cursor: pointer; display: flex; align-items: center;
  &:disabled { opacity: 0.5; cursor: not-allowed; }
`;
const Suggestions = styled.div`display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 0.5rem;`;
const Chip = styled.button`
  border: 1px solid ${(p) => p.theme.colors.border}; background: white; cursor: pointer;
  padding: 0.4rem 0.8rem; border-radius: 20px; font-size: 0.8rem; color: ${(p) => p.theme.colors.text.secondary};
`;

const STARTERS = [
  'Is my form right for Romanian deadlifts?',
  'Should I increase weight today?',
  "What's a substitute for cable flyes?",
];

export default function Coach() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: "Hey Gahan — I'm your coach. Ask me anything about today's session, form, or substitutions." },
  ]);
  const [input, setInput] = useState('');
  const [busy, setBusy] = useState(false);
  const endRef = useRef(null);

  useEffect(() => { endRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages, busy]);

  const send = async (text) => {
    const msg = (text ?? input).trim();
    if (!msg || busy) return;
    const history = messages.filter((m) => m.role !== 'system');
    setMessages((m) => [...m, { role: 'user', content: msg }]);
    setInput('');
    setBusy(true);
    try {
      const res = await trainerApi.chat(msg, history);
      setMessages((m) => [...m, { role: 'assistant', content: res.reply }]);
    } catch (e) {
      const detail = e.response?.data?.detail || 'Chat failed.';
      toast.error(detail);
      setMessages((m) => [...m, { role: 'assistant', content: detail }]);
    } finally {
      setBusy(false);
    }
  };

  return (
    <Container>
      <h1 style={{ marginBottom: '0.75rem' }}>Coach</h1>
      <Thread>
        {messages.map((m, i) => (
          <Bubble key={i} $me={m.role === 'user'}>{m.content}</Bubble>
        ))}
        {busy && <Bubble>Thinking…</Bubble>}
        <div ref={endRef} />
      </Thread>
      <Suggestions>
        {STARTERS.map((s) => <Chip key={s} onClick={() => send(s)}>{s}</Chip>)}
      </Suggestions>
      <Composer onSubmit={(e) => { e.preventDefault(); send(); }}>
        <Input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Ask your coach…" />
        <SendButton type="submit" disabled={busy}><Send size={18} /></SendButton>
      </Composer>
    </Container>
  );
}
