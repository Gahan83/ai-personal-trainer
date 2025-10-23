import React from 'react';
import styled from 'styled-components';
import { Target, TrendingUp, Calendar, Award } from 'lucide-react';

const DashboardContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
`;

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
`;

const StatCard = styled.div`
  background: white;
  padding: 1.5rem;
  border-radius: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
`;

const StatIcon = styled.div`
  width: 3rem;
  height: 3rem;
  background: ${props => props.theme.colors.primaryLight};
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: ${props => props.theme.colors.primary};
`;

const StatContent = styled.div`
  flex: 1;
`;

const StatValue = styled.h3`
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
  color: ${props => props.theme.colors.text.primary};
`;

const StatLabel = styled.p`
  margin: 0;
  color: ${props => props.theme.colors.text.secondary};
  font-size: 0.875rem;
`;

const Section = styled.section`
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
`;

const SectionTitle = styled.h2`
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: ${props => props.theme.colors.text.primary};
`;

const Dashboard = () => {
  const stats = [
    { icon: Target, value: '12', label: 'Workouts This Week' },
    { icon: TrendingUp, value: '85%', label: 'Goal Progress' },
    { icon: Calendar, value: '5', label: 'Days Streak' },
    { icon: Award, value: '3', label: 'Achievements' }
  ];

  return (
    <DashboardContainer>
      <h1>Dashboard</h1>
      
      <StatsGrid>
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <StatCard key={index}>
              <StatIcon>
                <Icon size={20} />
              </StatIcon>
              <StatContent>
                <StatValue>{stat.value}</StatValue>
                <StatLabel>{stat.label}</StatLabel>
              </StatContent>
            </StatCard>
          );
        })}
      </StatsGrid>

      <Section>
        <SectionTitle>Recent Workouts</SectionTitle>
        <p>Your recent workout history will appear here.</p>
      </Section>

      <Section>
        <SectionTitle>Today's Recommendations</SectionTitle>
        <p>AI-generated workout recommendations will appear here.</p>
      </Section>
    </DashboardContainer>
  );
};

export default Dashboard;
