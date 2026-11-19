# Sampati Community Edition

This is the **Community Edition** of Sampati - the open-source compliance automation platform built for India's regulators.

## What's Included (Free)

### Core Platform
- **Dashboard** - Overall compliance overview with statistics
- **Frameworks** - View compliance frameworks (SOC 2, ISO 27001, GDPR, HIPAA, DPDP, etc.)
- **Controls & Evidence** - View controls, track evidence attachments
- **Risk Assessment** - Basic risk visualization and tracking
- **Audits** - Schedule and track basic audit information
- **Settings** - User and organization settings

### Features
- Up to 5 compliance frameworks
- Up to 100 controls
- Basic risk assessment heat map
- Limited audit scheduling
- Standard templates for evidence types
- Community support via GitHub Discussions

### Technical
- React/Next.js frontend
- TypeScript
- Tailwind CSS
- Supabase backend API
- Open-source connectors

## What's Enterprise Only

### Premium Features
- **Advanced Connectors** - AWS, GCP, Azure, GitHub, Slack, Okta integrations
- **Real-time Evidence Collection** - Automated evidence gathering from connected systems
- **Custom Control Libraries** - Unlimited custom controls
- **Advanced Reporting** - Executive reports, customizable templates
- **Multi-tenancy** - Manage multiple organizations
- **SLA Support** - Production-grade deployment
- **Priority Support** - Dedicated support team
- **Advanced Risk Modeling** - Monte Carlo simulations, scenario analysis
- **Policy Automation** - Draft and review workflows
- **Audit Intelligence** - AI-powered findings analysis
- **Integration Hub** - 50+ pre-built integrations
- **Custom Branding** - White-label your instance

### Enterprise Connectors
- Cloud: AWS, GCP, Azure, OCI
- SaaS: GitHub, GitLab, Slack, Microsoft 365, Okta, Azure AD
- Security: Splunk, Datadog, CrowdStrike, SentinelOne
- Dev Tools: Jira, ServiceNow, Asana, Linear
- Finance: Stripe, PayPal, Razorpay

## Getting Started

### Prerequisites
- Node.js 18+ or Docker
- PostgreSQL 14+ (or use embedded SQLite for dev)

### Quick Start
```bash
# Clone the repo
git clone https://github.com/vayux/sampati.git
cd sampati

# Use the dev script
./scripts/dev.sh up

# Or install manually
npm install
npm run dev
```

### Development
```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run test         # Run tests
npm run lint         # Linting
```

## Upgrading to Enterprise

To unlock all features, visit [vayux.com/sampati-enterprise](https://vayux.com/sampati-enterprise)

## License

Apache-2.0 - See [LICENSE](../LICENSE) for details.

Sampati and VayuX names and logos are trademarks of VayuX Systems LLP.
