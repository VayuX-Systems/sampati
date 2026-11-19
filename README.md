# Sampati by VayuX

<p align="center">
  <img src="https://img.icons8.com/color/480/000000/exclamation.png" width="120" height="120">
  <br>
  <b>⚠️ ALPHA DEVELOPMENT RELEASE ⚠️</b>
  <br>
  <sub>The Open Source Compliance Automation Platform Built for India • <a href="https://github.com/VayuX-Systems/sampati">GitHub</a> • <a href="https://linkedin.com/company/vayux-systems">LinkedIn</a> • <a href="https://x.com/VayuXSystems">X</a></sub>
</p>

---

<div align="center">
  <img src="https://img.shields.io/badge/🚧-ALPHA DEVELOPMENT-red?style=for-the-badge">
  <img src="https://img.shields.io/badge/🔧-v0.0.1-alpha-yellow?style=for-the-badge">
  <img src="https://img.shields.io/badge/💻-Development%20Ongoing-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/⚠️-Not%20Production%20Stable-critical?style=for-the-badge">
</div>

---

## 🎯 Why Sampati?

> **Sampati isn't trying to copy Vanta or Drata.** We're solving a different problem.

Indian businesses face a unique challenge: world-class compliance tools with prices that don't work for us. Sampati changes that.

<p align="center">
  <img src="https://img.shields.io/badge/⚖️-DPDP%20Act%202023%20Native-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/🔐-CERT-In%20Support-purple?style=for-the-badge">
  <img src="https://img.shields.io/badge/₹-Indian%20Pricing-green?style=for-the-badge">
</p>

---

## 🚀 Quick Start (Alpha)

```bash
# Clone and run (may have issues!)
git clone https://github.com/VayuX-Systems/sampati.git
cd sampati
./scripts/dev.sh up

# OR Manual Setup
npm install
npm run dev
```

⚠️ **If something breaks, please [open an issue](https://github.com/VayuX-Systems/sampati/issues)!**

---

## 📊 Core Features (Alpha)

### Framework Library ✅
| Framework | Status | Controls |
|-----------|--------|----------|
| SOC 2 Type II | ✅ | 108 |
| ISO 27001:2022 | ✅ | 93 |
| GDPR | ✅ | 45 |
| HIPAA | ⚠️ | 52 |
| **DPDP Act 2023** | ⚠️ | 45 |
| CERT-In | ⚠️ | 52 |
| RBI CSCRF | ⚠️ | 58 |

### Controls Management ✅
- Control CRUD operations
- Evidence linking
- Status tracking (in progress)
- Bulk actions

### Evidence Collection ⚠️
- File upload/download
- Version tracking
- Expiry notifications
- S3 integration

### Risk Assessment ⚠️
- Heat map visualization
- Risk scoring
- Mitigation tracking

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│  sampati (Community Edition - DEVELOPING)│
├─────────────────────────────────────────┤
│  Sampati Enterprise (Planned)           │
├─────────────────────────────────────────┤
│  sampati-sdk (Developer Tools - WIP)    │
└─────────────────────────────────────────┘
```

### Technology Stack

| Layer | Technology | Status |
|-------|------------|--------|
| **Frontend** | React 18, Next.js 14, Tailwind CSS | ✅ Stable |
| **Backend** | FastAPI, Python 3.11 | ✅ Built |
| **Database** | PostgreSQL 14+, SQLModel | ✅ Working |
| **Cache** | Redis 7 | ✅ Implemented |
| **Storage** | MinIO/S3 Compatible | ⚠️ WIP |
| **Auth** | OAuth2, SSO, JWT | ⚠️ WIP |
| **Deploy** | Docker, Kubernetes | ⚠️ WIP |

---

## 🐛 Report Bugs (Crucial in Alpha!)

Since this is Alpha, we need your help finding issues:

- **🐛 Bug Reports**: [Open an issue](https://github.com/VayuX-Systems/sampati/issues)
- **💡 Feature Requests**: [Start a discussion](https://github.com/VayuX-Systems/sampati/discussions)
- **🧪 Security Issues**: security@vayux.com

---

## 📅 Development Roadmap

```
ALPHA (v0.0.1) → BETA (v0.5.0) → v1.0 GA (2025-Q2)
   [███████░░░░░] 70% Complete
         ↑
       This Week's Progress
```

### What's Being Built Now

- [ ] Full DPDP Act 2023 compliance controls
- [ ] CERT-In dashboard views
- [ ] RBI CSCRF framework templates
- [ ] Docker compose production readiness
- [ ] Test suite expansion
- [ ] Performance benchmarks

---

## 🤝 Join the Development

> **Built with ❤️ in India for the global compliance community**

| Platform | What You'll Find |
|----------|------------------|
| **💬 GitHub Discussions** | Talk to developers |
| **🐛 GitHub Issues** | Report bugs (critical in Alpha!) |
| **📖 Docs** | [Developer Guide](./DEVELOPERS.md) |
| **🐦 X (Twitter)** | [@VayuXSystems](https://x.com/VayuXSystems) |
| **👔 LinkedIn** | [VayuX Systems](https://linkedin.com/company/vayux-systems) |

---

## 📜 License

**Apache 2.0** — Commercial use, modification, and distribution allowed

Sampati and VayuX names/logos are trademarks of VayuX Systems LLP. See [LICENSE](LICENSE) for details.

---

<p align="center">
  <img src="https://img.icons8.com/ios-filled/240/000000/github.png" width="80" height="80">
  <br>
  <sub>🌍 50+ countries • 🤝 200+ contributors • 💡 Open source forever • ⚠️ Helping shape Alpha!</sub>
</p>
