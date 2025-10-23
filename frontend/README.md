# AI Personal Trainer - Frontend

React-based frontend for the AI Personal Trainer application.

## Features

- **Modern React** with hooks and functional components
- **Responsive Design** with styled-components
- **State Management** with React Query
- **Form Handling** with React Hook Form
- **Routing** with React Router
- **API Integration** with Axios

## Pages

- **Home** - Landing page with features overview
- **Login** - User authentication
- **Register** - User registration
- **Dashboard** - User dashboard with stats
- **Workouts** - Workout library and management
- **Profile** - User profile and settings

## Development

### Running the Application

```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test
```

### Environment Variables

Create a `.env` file in the frontend directory:

```
REACT_APP_API_URL=http://localhost:8000/api/v1
```

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Layout.js        # Main layout wrapper
│   ├── Header.js        # Top navigation
│   └── Sidebar.js       # Side navigation
├── pages/               # Page components
│   ├── Home.js          # Landing page
│   ├── Login.js         # Login page
│   ├── Register.js      # Registration page
│   ├── Dashboard.js     # User dashboard
│   ├── Workouts.js      # Workouts page
│   └── Profile.js       # User profile
├── hooks/               # Custom React hooks
│   └── useAuth.js       # Authentication hook
├── services/            # API services
│   └── api.js           # Axios configuration
├── styles/              # Styling
│   ├── theme.js         # Theme configuration
│   └── index.css        # Global styles
└── utils/               # Utility functions
    └── constants.js     # Application constants
```

## Styling

The application uses styled-components for styling with a centralized theme system. The theme includes:

- Color palette
- Typography
- Spacing
- Border radius
- Shadows

## State Management

- **React Query** for server state management
- **React Context** for authentication state
- **Local State** with useState and useReducer hooks
