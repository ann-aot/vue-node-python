# Vue 3 + TypeScript Professional Template

A production-ready setup for building Vue 3 applications with TypeScript, testing, Docker, ESLint, and Prettier.

---

## Features

- **Frontend:** Vue 3, TypeScript, Vite
- **API:** Node.js, TypeORM
- **Testing:** Vitest, Testing Library, Jest DOM
- **Code Quality:** ESLint, Prettier
- **Docker:** Multi-stage Dockerfile for production builds
- **Web Server:** Nginx (with SPA fallback to `index.html`)
- **Scripts:** Dev, Build, Preview, Lint, Format, Test

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Development](#development)
3. [Code Quality](#code-quality)
4. [Testing](#testing)
5. [Docker Deployment](#docker-deployment)
6. [Web Server Deployment](#web-server-deployment)
7. [Notes](#notes)

---

## Getting Started

### Install Dependencies

Each project manages its own dependencies:
```bash
cd frontend && npm install
cd api && npm install
```

### Available Scripts

- **Dev Server:** `npm run dev`
- **Build:** `npm run build`
- **Preview:** `npm run preview`
- **Lint:** `npm run lint`
- **Format:** `npm run format`
- **Test:** `npm run test`

### Running Development Servers
```bash
# Terminal 1 (frontend)
cd frontend && npm run dev

# Terminal 2 (frontend)
cd api && npm run start
```

Access locally:

- Frontend → http://localhost:${FRONTEND_DEV_PORT:-5173}
- API → http://localhost:${NODE_API_PORT:-5000}
- Backend → 
- Swagger UI →


---

## Development

Before committing code, make sure files are linted and formatted:
```bash
# Format & lint frontend
cd frontend && npm run lint
cd frontend && npm run lint:fix

# Format & lint api
cd api && npm run pretest
cd api && npm run lint
```

⚡ Husky + lint-staged will auto-run these checks on staged files during commits.

## Setting Up Husky and Linting

For the first time after cloning the project, run the following command to set up Husky:

```bash
npm run prepare
```
This will configure Git hooks for pre-commit checks.

---

To automatically fix linting issues in the code, run:

```bash
npm run lint:fix

```

This will apply ESLint and Prettier fixes where possible.

---

## Code Quality

- ESLint is configured for Vue 3 + TypeScript.
- Prettier is integrated with ESLint to auto-format code.

---

## Testing

- Vitest is configured with jsdom.
- Includes Testing Library + jest-dom for component testing.

---

## Docker Deployment

A multi-stage Dockerfile builds the Vue frontend and serves it with **Nginx**. For local development with both frontend + backend:
```bash
# Copy environment config
cp .env.sample .env

# Build and run
cd deployment/local
docker compose up -d --build
```

Access locally via docker:

- Frontend → http://localhost:${FRONTEND_DEV_PORT:-8080}
- API → http://localhost:${NODE_API_PORT:-5000}
- Backend → 
- Swagger UI →

---