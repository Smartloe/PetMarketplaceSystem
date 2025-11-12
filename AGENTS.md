# Repository Guidelines

## Project Structure & Module Organization

This is a full-stack pet marketplace system with separate frontend and backend directories:

- **Backend** (`backstage/pet_shop/`): Django REST API with MySQL database
  - `accounts/`: User authentication and profiles
  - `commodity/`: Product catalog and management
  - `trade/`: Order processing and payment handling
  - `customer_operation/`: Customer interactions and support
  - `merchant/`: Vendor management
  - `charts/`: Analytics and data visualization
  - `index/`: Homepage and landing content

- **Frontend** (`frontstage/pet_shop/`): Vue 3 application
  - `src/components/`: Reusable UI components
  - `src/views/`: Page-level components
  - `src/router/`: Vue Router configuration
  - `src/store/`: Vuex state management
  - `src/api/`: API service layer
  - `src/assets/`: Static assets and styles

## Build, Test, and Development Commands

### Backend (Django)
```bash
cd backstage/pet_shop
uv sync                    # Install dependencies
uv run python manage.py runserver 0.0.0.0:8000  # Start development server
uv run python manage.py migrate                 # Run database migrations
```

### Frontend (Vue 3)
```bash
cd frontstage/pet_shop
npm install                # Install dependencies
npm run serve              # Start development server (port 8080)
npm run build              # Build for production
npm run lint               # Run ESLint
```

## Coding Style & Naming Conventions

- **Backend**: Follow Django REST Framework patterns with 4-space indentation
- **Frontend**: Use Vue 3 Composition API with 2-space indentation
- **Naming**: Use snake_case for Python, camelCase for JavaScript
- **Formatting**: ESLint for frontend, no specific formatter for backend

## Testing Guidelines

- **Frontend**: ESLint configured with Vue 3 essential rules
- **Backend**: Django's built-in testing framework
- **Coverage**: No specific coverage requirements defined
- **Test Naming**: Use descriptive test names that explain expected behavior

## Commit & Pull Request Guidelines

- **Commit Messages**: Use descriptive, present-tense messages
- **PR Requirements**: Include clear descriptions of changes and screenshots for UI updates
- **Issue Linking**: Reference related issues in PR descriptions
- **Code Review**: Ensure all tests pass before requesting review

## Database Configuration

- MySQL database running on Windows host, accessed from WSL environment
- Connection details configured via environment variables:
  - `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_DATABASE`
  - `MYSQL_USER`, `MYSQL_PASSWORD`
- Database migrations managed via Django's migration system

## AI Integration

- LongCat AI API integration for pet consultation features
- API keys configured via `LONGCAT_API_KEY` environment variable
- AI endpoints exposed at `/api/ai/consult/`

## Environment Setup

- Backend uses `uv` for Python dependency management
- Frontend uses npm with Vue CLI
- Development servers run on localhost:8000 (backend) and 8080 (frontend)
- Cross-origin requests handled by django-cors-headers

## Agent-Specific Instructions

- When modifying backend code, ensure database migrations are created if models change
- Frontend API calls should use the configured backend URL
- AI features require proper API key configuration
- Database connectivity requires WSL-to-Windows network configuration
