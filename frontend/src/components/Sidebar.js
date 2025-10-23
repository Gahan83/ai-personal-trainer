import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import styled from 'styled-components';
import { Home, Dumbbell, User, Calendar, Target } from 'lucide-react';

const SidebarContainer = styled.aside`
  width: 250px;
  background: ${props => props.theme.colors.white};
  border-right: 1px solid ${props => props.theme.colors.border};
  padding: 2rem 0;
`;

const NavList = styled.ul`
  list-style: none;
  padding: 0;
  margin: 0;
`;

const NavItem = styled.li`
  margin-bottom: 0.5rem;
`;

const NavLink = styled(Link)`
  display: flex;
  align-items: center;
  padding: 1rem 2rem;
  color: ${props => props.theme.colors.text.secondary};
  text-decoration: none;
  transition: all 0.2s ease;
  border-left: 3px solid transparent;

  &:hover {
    background-color: ${props => props.theme.colors.background};
    color: ${props => props.theme.colors.primary};
  }

  &.active {
    background-color: ${props => props.theme.colors.primaryLight};
    color: ${props => props.theme.colors.primary};
    border-left-color: ${props => props.theme.colors.primary};
  }
`;

const NavIcon = styled.span`
  margin-right: 1rem;
  display: flex;
  align-items: center;
`;

const Sidebar = () => {
  const location = useLocation();

  const navItems = [
    { path: '/', icon: Home, label: 'Home' },
    { path: '/dashboard', icon: Target, label: 'Dashboard' },
    { path: '/workouts', icon: Dumbbell, label: 'Workouts' },
    { path: '/calendar', icon: Calendar, label: 'Calendar' },
    { path: '/profile', icon: User, label: 'Profile' },
  ];

  return (
    <SidebarContainer>
      <NavList>
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavItem key={item.path}>
              <NavLink 
                to={item.path} 
                className={location.pathname === item.path ? 'active' : ''}
              >
                <NavIcon>
                  <Icon size={20} />
                </NavIcon>
                {item.label}
              </NavLink>
            </NavItem>
          );
        })}
      </NavList>
    </SidebarContainer>
  );
};

export default Sidebar;
