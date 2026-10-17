# ProfilePulse — Product Requirements Document

**Status:** Final (v1 shipped)
**Owner:** Akshat Gupta
**One-liner:** A GitHub profile roaster: type any username and get a roast card built from that account's real public stats.

---

## 1. Problem

GitHub profile analysers all look the same: a table of repo counts and star totals that nobody screenshots. Developers do share things that are funny and about them. A roast is only funny if it's accurate, though, so it has to come from the account's real data, not a list of generic insults.

---

## 2. Goals (v1)

1. Accept any GitHub username and fetch the public profile plus up to 500 owned repos.
2. Compute stats: repo count, total stars, latest push, followers/following, distinct languages, fork ratio, average stars per repo.
3. Fire only the roast lines whose trigger condition is true for that profile.
4. Give each profile a title, a primary roast, secondary roasts and a verdict, stable across reloads.
5. Show a clear message for unknown users, rate limits and network errors.
6. Live, usable demo at [profilepulse.akshatgcodes.in](https://profilepulse.akshatgcodes.in), with the form on the landing page.

---

## 3. Non-Goals (explicit scope cuts)

- **Private repos or OAuth** — public data only, so there's no login.
- **Exact last-commit date** — approximated by the latest `pushed_at`, since the real thing needs per-repo commit history.
- **AI-written roasts** — rule-based only, so every line is grounded in data.
- **Image export** — users screenshot the card.

---

## 4. Users

**Primary:** Developers who want to roast themselves or a friend and share the result.

**Secondary:** Recruiters and engineers reviewing the project. They can roast any account, including their own, from the landing page.

---

## 5. User Stories

1. *As a developer,* I enter my username so that I see a roast card about my real GitHub activity.
2. *As a developer,* I reload the page so that I see the same card again, not a new random one.
3. *As a developer,* I roast a friend's username so that I can send them the card.
4. *As a visitor,* I mistype a username so that I see "No GitHub user found" instead of an error page.
5. *As a visitor,* I roast a profile with lots of stars so that I get a rare grudging compliment.

---

## 6. Functional Requirements

### 6.1 Input

- `GET` or `POST /roast` with `username`. Leading `@` and whitespace are stripped.
- An empty username shows "Enter a GitHub username to roast."

### 6.2 Data fetch

- `GET /users/{username}` for the profile. 404 → "No GitHub user found", 403 → rate-limit message, anything else not 200 → generic error.
- `GET /users/{username}/repos?type=owner&per_page=100`, paginated up to 5 pages (500 repos).
- Each request times out after 8 seconds.
- An optional `GITHUB_TOKEN` env var is sent as a bearer token.

### 6.3 Roast engine

- 11 independent triggers (see [ARCHITECTURE.md](ARCHITECTURE.md#4-roast-engine)).
- The title comes from the first matching pattern in priority order.
- Roast lines are shuffled with `random.Random(login)`, and the verdict uses `random.Random(login + "v")`.

### 6.4 Card

- Shows avatar, name, title, stats, the primary roast, the other fired roasts and the verdict.

---

## 7. Non-Functional Requirements

- **Latency:** two to six GitHub API calls per roast, each capped by an 8-second timeout.
- **Rate limits:** 60 requests/hour per IP without a token, 5,000 with one. A roast costs two or more requests.
- **Security:** usernames go into GitHub API URLs, and output is rendered through Jinja2 autoescaping. The token is server-side only.
- **Cost:** free. No paid APIs.

---

## 8. Success Metrics

| Metric | Target |
|---|---|
| Landing → roast card | One form submit |
| Stability | Same username, same card on reload |
| Errors | No stack trace ever reaches the browser |

---

## 9. Risks & Open Questions

- **Shared rate limit** — every visitor shares the server's GitHub quota. A token raises it to 5,000/hour.
- **Big accounts** — profiles with more than 500 repos are truncated.
- **Tone** — every line comments on account stats (stars, pushes, forks), never on the person.

---

## 10. v2 Candidates

- Cache API responses per username for a few minutes.
- A shareable image of the card.
- Contribution-calendar stats via the GraphQL API.

---

<div align="center">

<h3>Akshat Gupta</h3>

<a href="https://akshatgcodes.in"><img src="https://img.shields.io/badge/Website-akshatgcodes.in-111111?style=flat-square&logo=googlechrome&logoColor=white" alt="Website"></a>
<a href="https://linkedin.com/in/akshatgcodes"><img src="https://img.shields.io/badge/LinkedIn-akshatgcodes-0A66C2?style=flat-square" alt="LinkedIn"></a>
<a href="https://github.com/akshatgcodes"><img src="https://img.shields.io/badge/GitHub-akshatgcodes-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub"></a>
<a href="mailto:akshatgcodes@gmail.com"><img src="https://img.shields.io/badge/Email-akshatgcodes%40gmail.com-EA4335?style=flat-square&logo=gmail&logoColor=white" alt="Email"></a>

</div>
