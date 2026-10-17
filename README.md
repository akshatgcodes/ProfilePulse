<p align="center">
  <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24"
       fill="none" stroke="#f97316" stroke-width="1.5"
       stroke-linecap="round" stroke-linejoin="round">
    <path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/>
  </svg>
</p>

<h1 align="center">ProfilePulse</h1>

<p align="center">
  <strong>A GitHub profile roaster: type any username and get a roast card built from that account's real public stats.</strong>
</p>

<p align="center">
  <a href="https://profilepulse.akshatgcodes.in">
    <img src="https://img.shields.io/badge/live_demo-f97316-f97316?style=flat-square" alt="Live Demo">
  </a>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/GitHub_API-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub API">
  <img src="https://img.shields.io/badge/Next.js-black?style=flat-square&logo=next.js" alt="Next.js">
  <img src="https://img.shields.io/badge/license-GPL--3.0-f97316?style=flat-square" alt="License">
</p>

---

## What is ProfilePulse?

Most GitHub analysers give you a table of numbers. ProfilePulse pulls a profile and every public repo from the GitHub REST API, runs the numbers through a set of independent trigger conditions, and only fires the roast lines that are actually true for that account. Two usernames almost never get the same card, and the same username always gets the same one.

> **Live demo →** [profilepulse.akshatgcodes.in](https://profilepulse.akshatgcodes.in)
> Type a username on the landing page and hit **Roast them**. Try `octocat` or `torvalds`.

---

## What you get

- **Roast card** — avatar, a data-driven title ("The Ghost Committer", "The Digital Fossil"), repo count, total stars, last push, followers, languages and fork ratio.
- **Real triggers** — 11 independent conditions (≤5 stars, no bio, 90+ days since a push, mostly forks…), each gated on live API data.
- **Stable output** — lines are shuffled with a seed from the username, so a profile's card doesn't change on reload.
- **Clean errors** — unknown users, rate limits and network failures show a friendly message, never a stack trace.

---

## Stack

| Layer | Tech |
|---|---|
| Frontend | Jinja2 templates · plain CSS · Next.js 16 static landing page |
| Backend | Python · Flask 3 · `requests` |
| Data | GitHub REST API (`/users/{u}`, `/users/{u}/repos`) |
| Infra | Vercel (Python function + static landing) · GoDaddy DNS |

---

## Engineering Decisions

**Why rule-based roasts instead of an LLM?**
Every line is tied to a fact the API returned, so the card can be harsh without ever being wrong. It's also instant and free.

**Why seed the shuffle with the username?**
`random.Random(login)` gives each profile a stable order of roast lines and a stable verdict. Screenshots match what a friend sees when they try the same name.

**Why use the latest `pushed_at` for "last commit"?**
The REST API has no single "last commit" field. Walking commit history per repo would cost one request per repo against a 60-per-hour budget.

**What would you do differently in v2?**
Cache API responses per username for a few minutes, so a popular profile doesn't burn the rate limit on every reload.

---

## Docs

| Document | Description |
|---|---|
| [PRD](docs/PRD.md) | Product requirements — goals, user stories, non-goals |
| [Architecture](docs/ARCHITECTURE.md) | System design, data flow, component breakdown |
| [Decisions](docs/DECISIONS.md) | Every major technical decision and why |
| [Setup](docs/SETUP.md) | Local dev setup and env vars |
| [Deploy](docs/DEPLOY.md) | Production deployment, domains, rollback |
| [Contributing](CONTRIBUTING.md) | How to propose changes |
| [Changelog](CHANGELOG.md) | What changed in each release |
| [Security](SECURITY.md) | How to report a vulnerability |

---

<div align="center">

<h3>Akshat Gupta</h3>

<a href="https://akshatgcodes.in"><img src="https://img.shields.io/badge/Website-akshatgcodes.in-111111?style=flat-square&logo=googlechrome&logoColor=white" alt="Website"></a>
<a href="https://linkedin.com/in/akshatgcodes"><img src="https://img.shields.io/badge/LinkedIn-akshatgcodes-0A66C2?style=flat-square" alt="LinkedIn"></a>
<a href="https://github.com/akshatgcodes"><img src="https://img.shields.io/badge/GitHub-akshatgcodes-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub"></a>
<a href="mailto:akshatgcodes@gmail.com"><img src="https://img.shields.io/badge/Email-akshatgcodes%40gmail.com-EA4335?style=flat-square&logo=gmail&logoColor=white" alt="Email"></a>

</div>
