import React from 'react';
import styled from 'styled-components';
import { User, Bell, Settings } from 'lucide-react';

const HeaderContainer = styled.header`
  background: ${props => props.theme.colors.white};
  border-bottom: 1px solid ${props => props.theme.colors.border};
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const Title = styled.h1`
  color: ${props => props.theme.colors.primary};
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0;
`;

const HeaderActions = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
`;

const IconButton = styled.button`
  background: none;
  border: none;
  padding: 0.5rem;
  border-radius: 50%;
  cursor: pointer;
  color: ${props => props.theme.colors.text.secondary};
  transition: all 0.2s ease;

  &:hover {
    background-color: ${props => props.theme.colors.background};
    color: ${props => props.theme.colors.primary};
  }
`;

const Header = () => {
  return (
    <HeaderContainer>
      <Title>AI Personal Trainer</Title>
      <HeaderActions>
        <IconButton>
          <Bell size={20} />
        </IconButton>
        <IconButton>
          <Settings size={20} />
        </IconButton>
        <IconButton>
          <User size={20} />
        </IconButton>
      </HeaderActions>
    </HeaderContainer>
  );
};

export default Header;
