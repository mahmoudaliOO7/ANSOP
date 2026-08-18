# Frontend Application

React + TypeScript + Vite frontend for ANSOP security orchestration platform.

## Structure

```
frontend/
├── src/
│   ├── components/       # Reusable React components
│   ├── pages/            # Page components (Dashboard, Incidents, etc.)
│   ├── services/         # API client services
│   ├── hooks/            # Custom React hooks
│   ├── types/            # TypeScript type definitions
│   ├── styles/           # Global and component styles
│   ├── App.tsx           # Root application component
│   └── main.tsx          # Application entry point
├── public/               # Static assets
├── index.html            # HTML entry point
├── package.json          # Dependencies and scripts
├── tsconfig.json         # TypeScript configuration
├── vite.config.ts        # Vite build configuration
├── Dockerfile            # Container image definition
└── vitest.config.ts      # Test configuration
```

## Getting Started

### Local Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Docker Development

```bash
# Build and run with Docker Compose
cd ..
make up

# Access at http://localhost:5173
```

## Available Scripts

```bash
# Development
npm run dev           # Start Vite dev server

# Building
npm run build         # Build for production
npm run preview       # Preview production build locally

# Testing
npm run test          # Run tests with Vitest
npm run test:ui       # Run tests with UI
npm run test:coverage # Generate coverage report

# Code Quality
npm run lint          # Lint with ESLint
npm run format        # Format with Prettier
npm run type-check    # Check types with TypeScript
```

## Environment Configuration

Create `.env.local` for local overrides:

```bash
VITE_API_URL=http://localhost:8000/api/v1
VITE_APP_NAME=ANSOP
```

## API Integration

API client is configured in `src/services/api.ts`:

```typescript
import { api } from './services/api';

// GET request
const detections = await api.get('/detections');

// POST request
const result = await api.post('/detections', detectionData);

// With authentication (automatically added)
const response = await api.get('/incidents');
```

## Authentication

Authentication is handled via JWT tokens:

```typescript
import { useAuth } from './hooks/useAuth';

const { login, logout, user, token } = useAuth();

await login(username, password);
// Token automatically added to API requests
```

## Component Examples

### Dashboard Component

```typescript
import Dashboard from './pages/Dashboard';

// Displays metrics, pending approvals, recent events
```

### Incident List

```typescript
import IncidentList from './components/IncidentList';

<IncidentList filter={{ status: 'open' }} />
```

## Styling

- **Tailwind CSS** for utility-first styling
- **Shadcn/ui** for component library
- **CSS Modules** for component-scoped styles (optional)

## Testing

```bash
# Run tests
npm run test

# Watch mode
npm run test:watch

# Coverage
npm run test:coverage
```

## Performance

- Code splitting with dynamic imports
- Lazy loading of routes
- Image optimization
- Bundle analysis: `npm run build -- --analyze`

## Debugging

- React DevTools browser extension
- Redux DevTools (if using Redux)
- Vite debug mode: `npm run dev -- --debug`

## Building for Production

```bash
# Create optimized build
npm run build

# Output in dist/
# Serve with: npx serve -s dist
```

## Common Issues

**Port already in use**: Change `VITE_PORT` or kill the process using port 5173

**API connection error**: Verify `VITE_API_URL` matches backend URL

**Module not found**: Run `npm install` to ensure all dependencies are installed

## Deployment

See `docs/deployment.md` for production deployment guide.

---

**Phase**: 2 (Database Models & Migrations)  
**Status**: In Development
