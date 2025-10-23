import React from 'react';
import styled from 'styled-components';
import { User, Mail, Calendar, Target } from 'lucide-react';

const ProfileContainer = styled.div`
  max-width: 800px;
  margin: 0 auto;
`;

const ProfileCard = styled.div`
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
`;

const ProfileHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 2rem;
  margin-bottom: 2rem;
`;

const Avatar = styled.div`
  width: 5rem;
  height: 5rem;
  background: ${props => props.theme.colors.primaryLight};
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: ${props => props.theme.colors.primary};
  font-size: 2rem;
`;

const ProfileInfo = styled.div`
  flex: 1;
`;

const ProfileName = styled.h2`
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: ${props => props.theme.colors.text.primary};
`;

const ProfileEmail = styled.p`
  color: ${props => props.theme.colors.text.secondary};
  margin: 0;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
`;

const FormGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`;

const Label = styled.label`
  font-weight: 600;
  color: ${props => props.theme.colors.text.primary};
`;

const Input = styled.input`
  padding: 0.75rem;
  border: 1px solid ${props => props.theme.colors.border};
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: border-color 0.2s ease;

  &:focus {
    outline: none;
    border-color: ${props => props.theme.colors.primary};
  }
`;

const Button = styled.button`
  background: ${props => props.theme.colors.primary};
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
  align-self: flex-start;

  &:hover {
    background: ${props => props.theme.colors.primaryDark};
  }
`;

const Profile = () => {
  return (
    <ProfileContainer>
      <h1>Profile</h1>
      
      <ProfileCard>
        <ProfileHeader>
          <Avatar>
            <User size={32} />
          </Avatar>
          <ProfileInfo>
            <ProfileName>John Doe</ProfileName>
            <ProfileEmail>john.doe@example.com</ProfileEmail>
          </ProfileInfo>
        </ProfileHeader>

        <Form>
          <FormGroup>
            <Label htmlFor="name">Full Name</Label>
            <Input
              type="text"
              id="name"
              defaultValue="John Doe"
            />
          </FormGroup>

          <FormGroup>
            <Label htmlFor="email">Email</Label>
            <Input
              type="email"
              id="email"
              defaultValue="john.doe@example.com"
            />
          </FormGroup>

          <FormGroup>
            <Label htmlFor="birthdate">Birth Date</Label>
            <Input
              type="date"
              id="birthdate"
            />
          </FormGroup>

          <FormGroup>
            <Label htmlFor="fitness-goal">Fitness Goal</Label>
            <Input
              type="text"
              id="fitness-goal"
              placeholder="e.g., Build muscle, Lose weight, Stay fit"
            />
          </FormGroup>

          <Button type="submit">Update Profile</Button>
        </Form>
      </ProfileCard>
    </ProfileContainer>
  );
};

export default Profile;
