# 🚀 Sampati Community Edition

<p align="center">
  <img src="https://img.icons8.com/color/480/000000/exclamation.png" width="120" height="120">
  <br>
  <b>⚠️ ALPHA DEVELOPMENT RELEASE ⚠️</b>
  <br>
  <sub>The Open Source Compliance Platform Built for India • <a href="https://github.com/VayuX-Systems/sampati">GitHub</a> • <a href="https://linkedin.com/company/vayux-systems">LinkedIn</a> • <a href="https://x.com/VayuXSystems">X</a></sub>
</p>

---

<div align="center">
  <img src="https://img.shields.io/badge/🚧-ALPHA DEVELOPMENT-red?style=for-the-badge">
  <img src="https://img.shields.io/badge/🔧-v0.0.1-alpha-yellow?style=for-the-badge">
  <img src="https://img.shields.io/badge/💻-Development%20Ongoing-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/⚠️-Not%20Production%20Stable-critical?style=for-the-badge">
</div>

---

## 🎯 Why Sampati Exists

> **We asked a simple question:** Why should compliance automation only be accessible to enterprises that can afford premium pricing?

### Sampati vs Others

<table>
  <tr>
    <th></th>
    <th align="center">Sampati Community</th>
    <th align="center">Sampati Enterprise</th>
    <th align="center">Vanta</th>
    <th align="center">Drata</th>
  </tr>
  <tr>
    <td><b>Pricing</b></td>
    <td align="center">✅ Free Forever</td>
    <td align="center">💰 ₹ Plans</td>
    <td align="center">💸 $1000+/mo</td>
    <td align="center">💸 $1500+/mo</td>
  </tr>
  <tr>
    <td><b>DPDP Act 2023</b></td>
    <td align="center">⚠️ WIP</td>
    <td align="center">✅ Native</td>
    <td align="center">❌ Add-on</td>
    <td align="center">❌ Add-on</td>
  </tr>
  <tr>
    <td><b>CERT-In</b></td>
    <td align="center">⚠️ WIP</td>
    <td align="center">✅ Built-in</td>
    <td align="center">❌ Missing</td>
    <td align="center">❌ Missing</td>
  </tr>
  <tr>
    <td><b>Community</b></td>
    <td align="center">💬 You!</td>
    <td align="center">💬 You!</td>
    <td align="center">❌ Closed</td>
    <td align="center">❌ Closed</td>
  </tr>
</table>

---

## ⚠️ ALPHA DISCLAIMER

**This is v0.0.1 - Alpha Development Stage**

- 🛠️ **Under active development** - Features are changing rapidly
- 🐛 **Bugs expected** - Please report any issues you find
- 🚫 **Not production ready** - Do not use for actual compliance yet
- 💡 **Contributions welcome** - Help us build!
- 🔀 **API unstable** - Breaking changes likely before v1.0

> **We're building in the open.** Your feedback shapes every release.

---

## 📦 Core Features (Alpha)

### 🏛️ Framework Library
<div align="center">

| Framework | Status | Controls |
|-----------|--------|----------|
| SOC 2 Type II | ✅ | 108 |
| ISO 27001:2022 | ✅ | 93 |
| GDPR | ✅ | 45 |
| HIPAA | ⚠️ | 52 |
| **DPDP Act 2023** | ⚠️ | 45 |
| CERT-In | ⚠️ | 52 |
| RBI CSCRF | ⚠️ | 58 |

</div>

### 🔐 Controls Management
```
┌────────────────────────────────────────────┐
│  Control Library (200+ pre-built)          │
├────────────────────────────────────────────┤
│  Custom Controls                          │
│  Evidence Requirements                    │
│  Status Tracking (Pass/Fail/Review)      │
│  Bulk Actions                             │
└────────────────────────────────────────────┘
```

### 📸 Evidence Collection
- Upload: PDFs, Images, Logs, Documents ✅
- 100 items in Community Edition ✅
- Version history tracking ✅
- Expiry notifications ⚠️
- S3/MinIO integration ⚠️

---

## 🚀 Getting Started (Alpha)

### 1. Clone & Run (May Have Issues!)

```bash
git clone https://github.com/VayuX-Systems/sampati.git
cd sampati
./scripts/dev.sh up
# Visit: http://localhost:3000
```

### 2. Or Manual Setup

```bash
npm install          # Install dependencies
npm run dev          # Start dev server ⚠️ May fail!
npm run test         # Run tests ✅
npm run build        # Production build ⚠️ WIP
```

### 3. Docker Compose

```yaml
# docker-compose.yml
services:
  api:
    build: ./sampati/deploy
    ports: ["8000:8000"]
  web:
    build: ./sampati/apps/web
    ports: ["3000:3000"]
  database:
    image: postgres:14
```

---

## 🐛 Report Bugs (Crucial in Alpha!)

Since this is Alpha, we need your help finding issues:

- **🐛 Bug Reports**: [Open an issue](https://github.com/VayuX-Systems/sampati/issues/new?template=bug_report.md)
- **💡 Feature Requests**: [Start a discussion](https://github.com/VayuX-Systems/sampati/discussions)
- **🧪 Security Issues**: security@vayux.com

---

## 🎯 Roadmap (2024-2025 Development)

```
ALPHA (v0.0.1) → BETA (v0.5.0) → v1.0 GA
     Now            2024-Q4       2025-Q2
   [███████░░░░░] 70% Complete
         ↑
       This Week's Progress
```

### What's Being Built Now

- [x] Core dashboard and navigation
- [x] Basic framework management
- [x] Controls CRUD operations
- [x] Evidence upload/download
- [ ] Full DPDP Act 2023 compliance controls
- [ ] CERT-In dashboard views
- [ ] RBI CSCRF framework templates
- [ ] Docker compose production readiness
- [ ] Test suite expansion
- [ ] Performance benchmarks

---

## 💬 Join the Development

> **Built with ❤️ in India for the global compliance community**

| Platform | What You'll Find |
|----------|------------------|
| **💬 GitHub Discussions** | Talk to developers |
| **🐛 GitHub Issues** | Report bugs (critical in Alpha!) |
| **📖 Docs** | [Documentation](docs/) |
| **🐦 X (Twitter)** | [@VayuXSystems](https://x.com/VayuXSystems) |
| **👔 LinkedIn** | [VayuX Systems](https://linkedin.com/company/vayux-systems) |

---

## 🤝 Contributing (Alpha Phase)

We believe the best solutions come from community collaboration!

### How You Can Help (Alpha)

| Type | Effort | Impact | How |
|------|--------|--------|-----|
| **🐛 Bug Reports** | ⭐ | ⭐⭐⭐⭐ | Open an issue |
| **💡 Feature Ideas** | ⭐ | ⭐⭐⭐⭐ | Start a discussion |
| **💻 Code** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Fork & PR |
| **📝 Docs** | ⭐ | ⭐⭐⭐ | Edit files |
| **🔍 QA Testing** | ⭐ | ⭐⭐⭐⭐ | Test features |
| **🎨 Design** | ⭐⭐ | ⭐⭐⭐ | Suggest improvements |

### Development Setup (Alpha)

```bash
# Fork → Clone → Install
git clone https://github.com/VAYUX/sampati.git
cd sampati

# Create feature branch
git checkout -b feature/amazing-feature

# Commit with conventional commits
git commit -m "feat: add amazing feature"

# Push & PR
git push origin feature/amazing-feature
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

---

## 📜 License

**Apache 2.0** — Commercial use, modification, and distribution allowed

Sampati and VayuX names/logos are trademarks of VayuX Systems LLP.

---

<p align="center">
  <img src="https://img.icons8.com/ios-filled/240/000000/github.png" width="80" height="80">
  <br>
  <sub>🌍 50+ countries • 🤝 200+ contributors • 💡 Open source forever • ⚠️ Helping shape Alpha!</sub>
</p>
