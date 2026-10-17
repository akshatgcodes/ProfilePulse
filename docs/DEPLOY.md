# Deploying ProfilePulse

> **Live:** [profilepulse.akshatgcodes.in](https://profilepulse.akshatgcodes.in) · **Host:** Vercel · **Auto-deploy:** on push to `master`

For local development, see [SETUP.md](SETUP.md).

---

## 1. Architecture in production

| Piece | Runs on | Notes |
|---|---|---|
| Landing page | Vercel (static) | `landing/` built with `@vercel/static-build`, served at `/` |
| Flask app | Vercel (Python function) | `app.py` through `@vercel/python`; handles `/app` and `/roast` |
| Data | GitHub REST API | No database |
| DNS | GoDaddy | `profilepulse.akshatgcodes.in` → CNAME to Vercel |

---

## 2. Environment variables

Set in Vercel → Project `profilepulse` → Settings → Environment Variables (Production and Preview). The name is also in [`.env.example`](../.env.example).

| Variable | Required | Where it's set |
|---|---|---|
| `GITHUB_TOKEN` | ❌ (recommended) | Vercel env vars. Fine-grained GitHub token with no extra permissions. Without it, every visitor shares 60 requests/hour |

> After changing an env var, **redeploy**. Running deployments don't pick up new values.

---

## 3. First-time deploy

1. [vercel.com/new](https://vercel.com/new) → import `akshatgcodes/ProfilePulse`
2. Framework preset: **Other** · Root directory: `./` (the repo's `vercel.json` defines the builds)
3. Add `GITHUB_TOKEN`
4. Deploy. Every push to `master` now deploys to production, and every PR gets a preview URL.

---

## 4. Database migrations

None. ProfilePulse doesn't store anything.

---

## 5. Custom domain

`profilepulse.akshatgcodes.in` is set up with the setup toolkit:

```powershell
.\scripts\setup-subdomain.ps1 -Subdomain "profilepulse" -Platform Vercel -VercelProject "profilepulse"
```

Manual fallback: add the domain in Vercel → Project → Domains, then create a GoDaddy CNAME `profilepulse` → the target Vercel shows. HTTPS certificates are issued automatically once DNS resolves (2–10 min).

---

## 6. Verify a deploy

- [ ] `https://profilepulse.akshatgcodes.in` loads the landing page with the username form
- [ ] Roasting `octocat` shows a full card with stats and a verdict
- [ ] A made-up username shows the "No GitHub user found" page
- [ ] Reloading the same roast shows the same card

---

## 7. Rollback

| Host | How |
|---|---|
| Vercel | Dashboard → Deployments → pick the last good one → **Promote to Production** (or `vercel rollback`) |

After rolling back, note it in a commit or PR so the next push doesn't silently re-ship the broken version.

---

## 8. Monitoring & logs

- **Logs:** Vercel → Project `profilepulse` → Logs
- **Errors:** none yet beyond Vercel's function logs
- **Uptime:** none yet
- **Dependencies:** Dependabot opens weekly update PRs and a maintenance report is emailed every week (see `.github/workflows/`)

---

## Known production limitations

- All visitors share one GitHub API quota (60/hour without a token, 5,000 with one).
- Vercel prints a warning about the legacy `builds` config on every deploy. It's expected.

---

<div align="center">

<h3>Akshat Gupta</h3>

<a href="https://akshatgcodes.in"><img src="https://img.shields.io/badge/Website-akshatgcodes.in-111111?style=flat-square&logo=googlechrome&logoColor=white" alt="Website"></a>
<a href="https://linkedin.com/in/akshatgcodes"><img src="https://img.shields.io/badge/LinkedIn-akshatgcodes-0A66C2?style=flat-square" alt="LinkedIn"></a>
<a href="https://github.com/akshatgcodes"><img src="https://img.shields.io/badge/GitHub-akshatgcodes-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub"></a>
<a href="mailto:akshatgcodes@gmail.com"><img src="https://img.shields.io/badge/Email-akshatgcodes%40gmail.com-EA4335?style=flat-square&logo=gmail&logoColor=white" alt="Email"></a>

</div>
