import React from 'react';
import styled from 'styled-components';
import { Play, Clock, Target } from 'lucide-react';

const WorkoutsContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
`;

const WorkoutsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
`;

const WorkoutCard = styled.div`
  background: white;
  border-radius: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.2s ease;

  &:hover {
    transform: translateY(-2px);
  }
`;

const WorkoutImage = styled.div`
  height: 200px;
  background: linear-gradient(135deg, ${props => props.theme.colors.primary} 0%, ${props => props.theme.colors.secondary} 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 3rem;
`;

const WorkoutContent = styled.div`
  padding: 1.5rem;
`;

const WorkoutTitle = styled.h3`
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: ${props => props.theme.colors.text.primary};
`;

const WorkoutDescription = styled.p`
  color: ${props => props.theme.colors.text.secondary};
  margin-bottom: 1rem;
  line-height: 1.5;
`;

const WorkoutMeta = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
`;

const MetaItem = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: ${props => props.theme.colors.text.secondary};
  font-size: 0.875rem;
`;

const StartButton = styled.button`
  width: 100%;
  background: ${props => props.theme.colors.primary};
  color: white;
  padding: 0.75rem;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: background-color 0.2s ease;

  &:hover {
    background: ${props => props.theme.colors.primaryDark};
  }
`;

const Workouts = () => {
  const workouts = [
    {
      id: 1,
      title: 'Upper Body Strength',
      description: 'Build upper body strength with this comprehensive workout targeting chest, back, and arms.',
      duration: '45 min',
      difficulty: 'Intermediate',
      exercises: 8
    },
    {
      id: 2,
      title: 'Cardio Blast',
      description: 'High-intensity cardio workout to boost your heart rate and burn calories.',
      duration: '30 min',
      difficulty: 'Beginner',
      exercises: 6
    },
    {
      id: 3,
      title: 'Core Strength',
      description: 'Strengthen your core with targeted exercises for better stability and posture.',
      duration: '25 min',
      difficulty: 'Intermediate',
      exercises: 5
    }
  ];

  return (
    <WorkoutsContainer>
      <h1>Workouts</h1>
      
      <WorkoutsGrid>
        {workouts.map((workout) => (
          <WorkoutCard key={workout.id}>
            <WorkoutImage>
              <Target size={48} />
            </WorkoutImage>
            <WorkoutContent>
              <WorkoutTitle>{workout.title}</WorkoutTitle>
              <WorkoutDescription>{workout.description}</WorkoutDescription>
              
              <WorkoutMeta>
                <MetaItem>
                  <Clock size={16} />
                  {workout.duration}
                </MetaItem>
                <MetaItem>
                  <Target size={16} />
                  {workout.exercises} exercises
                </MetaItem>
              </WorkoutMeta>

              <StartButton>
                <Play size={16} />
                Start Workout
              </StartButton>
            </WorkoutContent>
          </WorkoutCard>
        ))}
      </WorkoutsGrid>
    </WorkoutsContainer>
  );
};

export default Workouts;
