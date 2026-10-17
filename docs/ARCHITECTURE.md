# ProfilePulse — Architecture

---

## 1. Stack

| Layer | Tech |
|---|---|
| Framework | Flask 3 (Python 3.12 on Vercel) |
| HTTP client | `requests`, 8-second timeout per call |
| Data source | GitHub REST API v3, optional bearer token |
| Templates | Jinja2 · plain CSS (`static/style.css`) |
| Landing page | Next.js 16 static export (`landing/`) · Tailwind CSS 4 |
| Hosting | Vercel: `@vercel/python` for Flask, `@vercel/static-build` for the landing page |

There's no database. Every roast is computed from a fresh API response.

---

## 2. Components

```
app.py            routes, GitHub API fetch with pagination and error mapping
roast.py          pure-Python roast engine: stats → triggers → title, roasts, verdict
templates/        base layout, username form, roast card, error page
static/style.css  roast card styling
landing/          Next.js landing page with a live username form
vercel.json       routes "/" to the landing page and everything else to Flask
```

### GitHub fetch (`app.py`)

`fetch_github_data(username)` calls `/users/{username}`, then pages through `/users/{username}/repos?type=owner` (100 per page, up to 5 pages). Every failure becomes a `GitHubLookupError` with a human-readable message, so routes never show a traceback.

### Roast engine (`roast.py`)

`build_roast_context(user, repos)` computes the stats, evaluates each trigger on its own, and returns a dict for the template: stats, `title`, `primary_roast`, `secondary_roasts` and `verdict`. It doesn't import Flask.

---

## 3. Data Flow

```
[Landing form] GET /roast?username=octocat
    --> fetch_github_data
          GET /users/octocat
          GET /users/octocat/repos?page=1..5
    --> build_roast_context(user, repos)
          stats --> 11 triggers --> roast lines (shuffled with seed "octocat")
          stats --> title (first matching pattern)
          seed "octocatv" --> verdict
    --> render roast.html
```

1. The landing page's form submits `username` to `/roast` on the same domain.
2. Flask strips whitespace and a leading `@`, then fetches the profile and repos.
3. The roast engine works out the stats and fires every true trigger.
4. Lines are ordered with `random.Random(login).shuffle`, so the order is stable for that user.
5. The card renders. Errors render `error.html` with the message from `GitHubLookupError`.

---

## 4. Roast Engine

**Stats:** repo count, total stars, distinct languages, latest `pushed_at` (days ago), followers, following, fork ratio, original-repo count, average stars per repo, whether any repo has a description, whether there's a bio.

**Triggers** (each one is checked independently):

| Pattern | Condition |
|---|---|
| Starless | Repos exist and total stars is 0, or ≤ 5 |
| No bio | Bio is empty |
| Monolingual / no language | Exactly one, or zero, languages across repos |
| Stale | Last push ≥ 90 days ago (≥ 365 is worse) |
| No followers | 0 followers |
| Follow-for-follow | Following > 10× followers and ≥ 20 following |
| Repo hoarder | ≥ 15 repos and ≤ 10 total stars |
| No descriptions | No repo has a description |
| Fork-heavy | Fork ratio ≥ 0.6 and ≤ 3 original repos |
| Compliment | Average stars per repo ≥ 50 |

**Title** (first match wins): no repos → The Ghost · last push ≥ 365 days → The Digital Fossil · 0 stars with ≥ 5 repos → The Ghost Committer · one language with ≥ 3 repos → The `<Language>` Loyalist · fork ratio ≥ 0.6 with ≥ 5 repos → The Serial Forker · ≥ 15 repos and ≤ 10 stars → The Repo Hoarder · average ≥ 50 stars → The Low-Key Legend · 0 followers → The Lone Wolf · otherwise The Mysterious Committer.

---

## 5. Routes

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Landing page in production. Locally, redirects to `/app` |
| `GET` | `/app` | Username form |
| `GET/POST` | `/roast` | Fetch, roast and render the card (or an error page) |

---

## 6. Security

- **Output:** all GitHub data (bio, repo names, descriptions) goes through Jinja2 autoescaping.
- **Token:** `GITHUB_TOKEN` is read from the environment and only sent to `api.github.com`. It never reaches the browser.
- **Secrets:** the token is a Vercel env var. `.env*` files are gitignored.
- **Input:** the username is only used in GitHub API paths, and GitHub validates it.

---

## 7. Error Handling & Reliability

| Failure | Behaviour |
|---|---|
| Empty username | Error page: "Enter a GitHub username to roast." |
| User not found (404) | Error page with the username |
| Rate limited (403) | Error page explaining the limit |
| Network error or timeout | Error page: "Couldn't reach GitHub right now…" |
| Repos page fails mid-way | Roast uses the repos fetched so far |

---

## 8. Deployment

1. The Vercel project `profilepulse` is linked to `akshatgcodes/ProfilePulse` and deploys every push to `master`.
2. `vercel.json` builds `landing/` as a static export served at `/`, serves `static/**` as files, and sends everything else to `app.py`.
3. `GITHUB_TOKEN` (optional) is set in the Vercel env vars.

Full steps are in [DEPLOY.md](DEPLOY.md).

---

## 9. Explicit Scope Cuts

- **Caching** — every roast hits the API.
- **GraphQL contribution data** — the REST API is enough for v1.
- **Database** — nothing is stored.

---

<div align="center">

<h3>Akshat Gupta</h3>

<a href="https://akshatgcodes.in"><img src="https://img.shields.io/badge/Website-akshatgcodes.in-111111?style=flat-square&logo=googlechrome&logoColor=white" alt="Website"></a>
<a href="https://linkedin.com/in/akshatgcodes"><img src="https://img.shields.io/badge/LinkedIn-akshatgcodes-0A66C2?style=flat-square" alt="LinkedIn"></a>
<a href="https://github.com/akshatgcodes"><img src="https://img.shields.io/badge/GitHub-akshatgcodes-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub"></a>
<a href="mailto:akshatgcodes@gmail.com"><img src="https://img.shields.io/badge/Email-akshatgcodes%40gmail.com-EA4335?style=flat-square&logo=gmail&logoColor=white" alt="Email"></a>

</div>
