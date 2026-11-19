# 🧑‍💻 Sampati Developer Guide

<p align="center">
  <img src="https://img.icons8.com/color/480/000000/code.png" width="120" height="120">
  <br>
  <b>Building Sampati Together</b>
  <br>
  <sub>Open source compliance automation for India's regulators</sub>
</p>

---

## 🎯 Table of Contents

1. [Getting Started](#-getting-started)
2. [Project Structure](#-project-structure)
3. [Technology Stack](#-technology-stack)
4. [Development Workflow](#-development-workflow)
5. [Architecture](#-architecture)
6. [Code Standards](#-code-standards)
7. [Testing](#-testing)
8. [Contributing](#-contributing)
9. [Roadmap](#-roadmap)

---

## 🚀 Getting Started

### Prerequisites

```yaml
Node.js: 18+ or Docker
npm: 8+ or yarn
PostgreSQL: 14+ (or use embedded SQLite for dev)
pnpm: 8+ (recommended)
```

### Quick Setup

```bash
# Clone the repo
git clone https://github.com/VayuX-Systems/sampati.git
cd sampati

# Install dependencies (using pnpm)
pnpm install

# Start development environment
./scripts/dev.sh up

# Or use Docker
docker compose -f deploy/docker-compose.yml up -d
```

### Available Scripts

| Script | Description |
|--------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run test` | Run tests |
| `npm run lint` | Run linter |
| `npm run type-check` | TypeScript type checking |
| `./scripts/dev.sh up` | Start full dev environment |
| `./scripts/dev.sh down` | Stop dev environment |

---

## 🏗️ Project Structure

```
sampati/
├── apps/                          # Applications
│   ├── api/                       # Backend API (FastAPI)
│   │   ├── src/                   # Source code
│   │   ├── tests/                 # Test files
│   │   └── pyproject.toml         # Python dependencies
│   │
│   ├── web/                       # Frontend (Next.js)
│   │   ├── src/
│   │   │   ├── app/               # App Router pages
│   │   │   ├── components/        # React components
│   │   │   ├── types/             # TypeScript types
│   │   │   ├── mocks/             # Mock data
│   │   │   └── lib/               # Utilities
│   │   ├── next.config.js
│   │   └── package.json
│   │
│   └── worker/                    # Background jobs
│
├── packages/                      # Shared packages
│   ├── core-domain/               # Domain models
│   ├── rules-engine/              # Compliance rules
│   ├── ledger/                    # Evidence storage
│   ├── plugin-host/               # Plugin system
│   └── extension-points/          # Extension APIs
│
├── scripts/                       # Development scripts
├── docs/                          # Documentation
├── deploy/                        # Docker configs
└── tests/                         # End-to-end tests
```

---

## 🛠️ Technology Stack

### Frontend (Web App)

| Tool | Version | Purpose |
|------|---------|---------|
| **React** | 18.2+ | UI Library |
| **Next.js** | 14.x | App Router, SSR |
| **Tailwind CSS** | 3.x | Styling |
| **TypeScript** | 5.x | Type Safety |
| **shadcn/ui** | Latest | Component Library |
| **lucide-react** | Latest | Icons |
| **zod** | Latest | Validation |

### Backend (API)

| Tool | Version | Purpose |
|------|---------|---------|
| **Python** | 3.11 | Backend language |
| **FastAPI** | 0.100+ | API framework |
| **SQLModel** | 0.0.14 | ORM |
| **Pydantic** | 2.x | Data validation |
| **Redis** | 7.x | Caching |
| **PostgreSQL** | 14+ | Database |

### Development Tools

| Tool | Purpose |
|------|---------|
| **pnpm** | Package manager |
| **Docker** | Containerization |
| **uv** | Python package manager |
| **pytest** | Testing |
| **ruff** | Linting/formatting |
| **pre-commit** | Git hooks |

---

## 🔄 Development Workflow

### 1. Create Feature Branch

```bash
# Always start from main
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/your-feature-name
```

### 2. Follow Conventional Commits

```bash
# Good commit messages
feat: add DPDP Act framework support
fix: resolve evidence upload failing
docs: update CONTRIBUTING.md
refactor: optimize risk scoring algorithm
test: add unit tests for controls
chore: update dependencies
```

### 3. Code Changes

- Write tests for new features
- Update documentation
- Follow code standards (see below)
- Run lint and type-check before PR

### 4. Create Pull Request

```bash
git push origin feature/your-feature-name
# Open PR on GitHub
```

---

## 🏗️ Architecture

### System Architecture

```
┌─────────────────┐
│   Web Client    │  (Next.js)
└────────┬────────┘
         │ API Calls
┌────────▼────────┐
│     API Gateway │  (FastAPI)
└────────┬────────┘
         │
   ┌─────┴─────┐
   ▼           ▼
┌───────┐  ┌─────────┐
│  Auth │  │ Business│
│ (JWT) │  │ Logic   │
└───┬───┘  └────┬────┘
    │           │
    └─────┬─────┘
          ▼
┌──────────────────┐
│   Data Storage   │
├──────────────────┤
│ PostgreSQL (SQL) │
│ Redis (Cache)    │
│ MinIO (S3)       │
└──────────────────┘
```

### Key Design Principles

1. **Domain-Driven Design**: Core entities in `core-domain` package
2. **Hexagonal Architecture**: Ports and adapters pattern
3. **CQRS**: Separate read/write models for compliance rules
4. **Plugin System**: Extensible connector architecture
5. **Event Sourcing**: Audit trails for all actions

### Package Structure

Each package follows this pattern:

```
packages/
└── core-domain/
    ├── pyproject.toml
    ├── README.md
    └── src/
        └── sampati_core_domain/
            ├── __init__.py
            ├── models/
            │   ├── control.py
            │   ├── framework.py
            │   └── evidence.py
            ├── services/
            │   ├── risk_service.py
            │   └── compliance_service.py
            └── errors.py
```

---

## ✍️ Code Standards

### Frontend (TypeScript/React)

```typescript
// Component structure
interface Props {
  title: string;
  status: FrameworkStatus;
  controls: Control[];
}

export function FrameworkCard({ title, status, controls }: Props) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        <StatusBadge status={status} />
      </CardHeader>
      <CardBody>
        <ProgressBar value={complianceScore} />
      </CardBody>
    </Card>
  );
}
```

### Backend (Python)

```python
# Model structure
from sqlmodel import SQLModel, Field
from enum import Enum

class FrameworkStatus(str, Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non-compliant"
    IN_PROGRESS = "in-progress"

class Framework(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    code: str
    status: FrameworkStatus
    total_controls: int
```

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| **Files** | kebab-case | `framework-service.py` |
| **Classes** | PascalCase | `FrameworkService` |
| **Functions** | camelCase | `getFrameworkById` |
| **Variables** | camelCase | `userList` |
| **Constants** | UPPER_SNAKE | `MAX_CONTROL_COUNT` |

---

## 🧪 Testing

### Run All Tests

```bash
# Backend tests
cd apps/api
pytest

# Frontend tests
cd apps/web
npm run test

# End-to-end tests
cd tests
npm run test:e2e
```

### Test Coverage Goals

| Area | Target Coverage |
|------|-----------------|
| Core Domain | 90%+ |
| Backend API | 80%+ |
| Frontend Components | 70%+ |
| Integration Tests | 60%+ |

### Writing Tests

#### Backend (pytest)

```python
def test_framework_creation():
    framework = Framework(
        name="SOC 2",
        code="SOC2",
        status=FrameworkStatus.IN_PROGRESS
    )
    assert framework.name == "SOC 2"
```

#### Frontend (Vitest)

```typescript
import { render, screen } from '@testing-library/react'
import { FrameworkCard } from './FrameworkCard'

test('renders framework title', () => {
  render(<FrameworkCard title="SOC 2" status="in-progress" controls={[]} />)
  expect(screen.getByText('SOC 2')).toBeInTheDocument()
})
```

---

## 🤝 Contributing

### How to Get Started

1. **Read this guide** (you're doing great!)
2. **Check existing issues** for good first tasks
3. **Join discussions** for feature ideas
4. **Create a fork** and start coding!

### Good First Issues

Look for the `good-first-issue` label on GitHub Issues:
https://github.com/VayuX-Systems/sampati/issues?q=is:issue+is:open+label:good-first-issue

### Contribution Types

| Type | Effort | Impact | How |
|------|--------|--------|-----|
| **🐛 Bug Reports** | ⭐ | ⭐⭐⭐⭐ | Open an issue |
| **💡 Feature Ideas** | ⭐ | ⭐⭐⭐⭐ | Start a discussion |
| **💻 Code** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Fork & PR |
| **📝 Docs** | ⭐ | ⭐⭐⭐ | Edit files |
| **🔍 QA Testing** | ⭐ | ⭐⭐⭐⭐ | Test features |
| **🎨 Design** | ⭐⭐ | ⭐⭐⭐ | Suggest improvements |

### Pull Request Process

1. Create a feature branch
2. Make changes with tests
3. Run tests and lint
4. Update documentation
5. Submit PR with clear description

---

## 📅 Roadmap

```
ALPHA (v0.0.1) → BETA (v0.5.0) → v1.0 GA (2025-Q2)
   [███████░░░░░] 70% Complete
         ↑
       This Week's Progress
```

### Q4 2024 - Alpha Development
- [x] Core dashboard and navigation
- [x] Basic framework management
- [x] Controls CRUD operations
- [x] Evidence upload/download
- [ ] Full DPDP Act 2023 compliance controls
- [ ] CERT-In dashboard views

### Q1 2025 - Beta Preparation
- [ ] RBI CSCRF framework templates
- [ ] Audit readiness scoring
- [ ] Risk assessment heat map
- [ ] Docker compose production readiness

### Q2 2025 - v1.0 Target
- [ ] Full feature parity with Vanta/Drata free tier
- [ ] Production readiness
- [ ] Community adoption
- [ ] Enterprise feature planning

---

## 🤝 Get in Touch

> **Built with ❤️ in India for the global compliance community**

| Platform | Handle |
|----------|--------|
| **GitHub** | [VayuX-Systems/sampati](https://github.com/VayuX-Systems/sampati) |
| **LinkedIn** | [@vayuxsystems](https://linkedin.com/company/vayux-systems) |
| **X/Twitter** | [@VayuXSystems](https://x.com/VayuXSystems) |
| **Email** | hello@vayux.com |

---

<p align="center">
  <img src="https://img.icons8.com/ios-filled/240/000000/github.png" width="80" height="80">
  <br>
  <sub>🌍 50+ countries • 🤝 200+ contributors • 💡 Open source forever • ⚠️ Helping shape Alpha!</sub>
</p>
