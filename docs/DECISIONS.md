# Engineering Decisions — ProfilePulse

---

## Decision 1 — Rule-based roasts, not an LLM

**Context:** The whole app is the roast. It has to be funny, but a roast that gets the facts wrong ("you have no stars" to someone with 2,000) just looks broken.

**Decision:** `roast.py` evaluates independent boolean triggers over computed stats and only fires the lines whose condition is true.

**Reason:** Every line is grounded in a number the API returned, so the card can be harsh without being wrong. It also means no API key, no cost and no latency beyond GitHub's own.

**Tradeoff:** The line bank is finite, so frequent users will recognise lines. Adding a pattern means writing code, not editing a prompt.

---

## Decision 2 — Deterministic shuffle seeded by the username

**Context:** With several triggers firing, the order of lines and the verdict could be random on every reload. Then a screenshot wouldn't match what a friend sees.

**Decision:** `random.Random(login).shuffle(roasts)` for the lines and `random.Random(login + "v")` for the verdict.

**Reason:** Each profile gets a stable card that still varies across users. No storage is needed to make it stable.

**Tradeoff:** A profile's card only changes when its stats change. Nobody gets a different roast just by reloading.

---

## Decision 3 — Latest `pushed_at` as "last commit"

**Context:** The card shows how long it's been since the user last committed.

**Decision:** Use the most recent `pushed_at` across the user's repos, which comes back in the repos listing anyway.

**Reason:** The REST API has no global "last commit" field. Walking commit history would cost one request per repo against a 60-per-hour unauthenticated budget.

**Tradeoff:** Pushes to forks or branches count, and private activity doesn't. It's an approximation, and the docs say so.

---

## Decision 4 — Every API failure becomes a friendly message

**Context:** GitHub returns 404 for unknown users, 403 when rate-limited, and can time out.

**Decision:** `fetch_github_data` maps each case to a `GitHubLookupError` with a human message. Routes catch it and render `error.html`. Each request has an 8-second timeout.

**Reason:** A visitor who mistypes a name, or hits the shared limit, sees a clear explanation, never a stack trace.

**Tradeoff:** A repos page that fails mid-way ends pagination quietly, so the card uses the repos fetched so far instead of failing outright.

---

## Decision 5 — Landing page and app on one Vercel project

**Context:** The landing page used to be a separate site describing the app.

**Decision:** One Vercel project. `vercel.json` serves the static landing page at `/`, the landing hero has a live form that submits to `/roast`, and the app's own form moved to `/app`.

**Reason:** A visitor can roast someone from the first screen, on one domain, with no extra click.

**Tradeoff:** It uses Vercel's legacy `builds` config, which shows a warning on deploy.

---

## What I'd do differently in v2

- **Cache per username** — a short in-memory or KV cache would stop popular profiles burning the shared rate limit.
- **GraphQL** — one GraphQL query could fetch the profile, repos and real contribution counts together.
- **Tests for `roast.py`** — it's pure and deterministic, which makes it ideal for snapshot tests.

---

## Explicit non-decisions (deferred to v2)

| Feature | Why deferred |
|---|---|
| Image export of the card | Screenshots work. Server-side image rendering adds a heavy dependency |
| OAuth / private repos | Public data is the point. Private repos would need a login and a privacy story |
| More than 500 repos | Five pages covers almost every account and keeps a roast to six requests at most |

---

<div align="center">

<h3>Akshat Gupta</h3>

<a href="https://akshatgcodes.in"><img src="https://img.shields.io/badge/Website-akshatgcodes.in-111111?style=flat-square&logo=googlechrome&logoColor=white" alt="Website"></a>
<a href="https://linkedin.com/in/akshatgcodes"><img src="https://img.shields.io/badge/LinkedIn-akshatgcodes-0A66C2?style=flat-square" alt="LinkedIn"></a>
<a href="https://github.com/akshatgcodes"><img src="https://img.shields.io/badge/GitHub-akshatgcodes-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub"></a>
<a href="mailto:akshatgcodes@gmail.com"><img src="https://img.shields.io/badge/Email-akshatgcodes%40gmail.com-EA4335?style=flat-square&logo=gmail&logoColor=white" alt="Email"></a>

</div>
