# Local Setup — ProfilePulse

> **Just want to try it?** Use the live demo at [profilepulse.akshatgcodes.in](https://profilepulse.akshatgcodes.in). No setup needed.
> This guide is for running ProfilePulse locally or self-hosting it.

---

## Prerequisites

- Python 3.8+
- Node.js 20+, only if you want to build the landing page

---

## 1. Clone and install

```bash
git clone https://github.com/akshatgcodes/ProfilePulse
cd ProfilePulse
pip install -r requirements.txt
```

---

## 2. Environment variables

Nothing is required. One optional variable raises the GitHub API limit:

| Variable | Where to get it |
|---|---|
| `GITHUB_TOKEN` | Optional. [github.com/settings/personal-access-tokens](https://github.com/settings/personal-access-tokens) → fine-grained token with no extra permissions (public data only). Raises the limit from 60 to 5,000 requests/hour |

```bash
export GITHUB_TOKEN="github_pat_..."
```

---

## 3. Run locally

```bash
python app.py
```

Open `http://localhost:5000`. Locally, `/` redirects to the username form at `/app`, since the landing page is only built at deploy time. Try `octocat`, `torvalds` or your own username.

To preview the landing page:

```bash
cd landing && npm install && npm run dev   # http://localhost:3000
```

---

## 4. Deploy to production

See [DEPLOY.md](DEPLOY.md) for production deployment, custom domain and rollback steps.

---

## Testing

There's no automated test suite yet. CI checks that every Python file compiles and that the landing page lints and builds. To check a change by hand: roast `octocat` (many stars), a brand-new account (no repos) and a misspelled name (not found), and confirm each card or error page looks right.

---

## Known local-only limitations

- `/` doesn't show the landing page locally. In production `vercel.json` routes it to the static export.
- Without `GITHUB_TOKEN`, you get 60 API requests an hour, which is about 30 roasts.

---

<div align="center">

<h3>Akshat Gupta</h3>

<a href="https://akshatgcodes.in"><img src="https://img.shields.io/badge/Website-akshatgcodes.in-111111?style=flat-square&logo=googlechrome&logoColor=white" alt="Website"></a>
<a href="https://linkedin.com/in/akshatgcodes"><img src="https://img.shields.io/badge/LinkedIn-akshatgcodes-0A66C2?style=flat-square" alt="LinkedIn"></a>
<a href="https://github.com/akshatgcodes"><img src="https://img.shields.io/badge/GitHub-akshatgcodes-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub"></a>
<a href="mailto:akshatgcodes@gmail.com"><img src="https://img.shields.io/badge/Email-akshatgcodes%40gmail.com-EA4335?style=flat-square&logo=gmail&logoColor=white" alt="Email"></a>

</div>
