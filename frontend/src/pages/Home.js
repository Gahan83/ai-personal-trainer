import React from 'react';
import styled from 'styled-components';
import { Link } from 'react-router-dom';
import { Dumbbell, Target, TrendingUp, Users } from 'lucide-react';

const HomeContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
`;

const HeroSection = styled.section`
  text-align: center;
  padding: 4rem 0;
  background: linear-gradient(135deg, ${props => props.theme.colors.primary} 0%, ${props => props.theme.colors.secondary} 100%);
  color: white;
  border-radius: 1rem;
  margin-bottom: 3rem;
`;

const HeroTitle = styled.h1`
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 1rem;
`;

const HeroSubtitle = styled.p`
  font-size: 1.25rem;
  margin-bottom: 2rem;
  opacity: 0.9;
`;

const CTAButton = styled(Link)`
  display: inline-block;
  background: white;
  color: ${props => props.theme.colors.primary};
  padding: 1rem 2rem;
  border-radius: 0.5rem;
  text-decoration: none;
  font-weight: 600;
  transition: transform 0.2s ease;

  &:hover {
    transform: translateY(-2px);
  }
`;

const FeaturesGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 3rem;
`;

const FeatureCard = styled.div`
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
`;

const FeatureIcon = styled.div`
  width: 4rem;
  height: 4rem;
  background: ${props => props.theme.colors.primaryLight};
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  color: ${props => props.theme.colors.primary};
`;

const FeatureTitle = styled.h3`
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: ${props => props.theme.colors.text.primary};
`;

const FeatureDescription = styled.p`
  color: ${props => props.theme.colors.text.secondary};
  line-height: 1.6;
`;

const Home = () => {
  const features = [
    {
      icon: Target,
      title: 'Personalized Workouts',
      description: 'AI-powered workout plans tailored to your fitness goals and preferences.'
    },
    {
      icon: TrendingUp,
      title: 'Progress Tracking',
      description: 'Monitor your fitness journey with detailed analytics and progress reports.'
    },
    {
      icon: Dumbbell,
      title: 'Exercise Library',
      description: 'Access a comprehensive database of exercises with proper form guidance.'
    },
    {
      icon: Users,
      title: 'Expert Guidance',
      description: 'Get professional fitness advice and motivation from our AI trainer.'
    }
  ];

  return (
    <HomeContainer>
      <HeroSection>
        <HeroTitle>Your AI Personal Trainer</HeroTitle>
        <HeroSubtitle>
          Achieve your fitness goals with personalized workout plans and expert guidance
        </HeroSubtitle>
        <CTAButton to="/register">Get Started Today</CTAButton>
      </HeroSection>

      <FeaturesGrid>
        {features.map((feature, index) => {
          const Icon = feature.icon;
          return (
            <FeatureCard key={index}>
              <FeatureIcon>
                <Icon size={24} />
              </FeatureIcon>
              <FeatureTitle>{feature.title}</FeatureTitle>
              <FeatureDescription>{feature.description}</FeatureDescription>
            </FeatureCard>
          );
        })}
      </FeaturesGrid>
    </HomeContainer>
  );
};

export default Home;
