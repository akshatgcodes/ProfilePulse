# ProfilePulse

A GitHub profile roaster. Type any GitHub username into the web UI —
ProfilePulse fetches their public data via the GitHub REST API and generates
a **roast card**: a visually styled report that mixes real stats with
savage (but accurate) commentary.

- **Month:** September 2023
- **Language:** Python
- **Type:** Web App

## What it does

Enter a GitHub username on the home page. ProfilePulse calls the GitHub
REST API to pull public profile data (bio, followers, following) and every
public repo (stars, language, fork status, last push date), then renders a
roast card with:

- 👤 Username, avatar, and a procedurally-assigned title (e.g. "The Ghost
  Committer", "The Repo Hoarder", "The Digital Fossil")
- 📦 Repo count, ⭐ total stars, 🗓️ last commit recency, 👥 followers,
  🧑‍💻 language count, 🍴 fork ratio
- 🔥 A primary roast line plus secondary "also noted" roasts
- 💀 A closing verdict

## X Factor: procedural, data-driven roasting

Every other GitHub analyzer gives you a boring table of numbers.
ProfilePulse's roast engine (`roast.py`) evaluates the *real* stats against
a bank of independent trigger conditions and only fires the lines whose
condition is actually true for that profile:

| Real data pattern | Roast trigger |
| --- | --- |
| Repos exist but 0–5 total stars | "23 repos, 4 stars, and the audacity to have a bio." |
| No bio set | "Even your repos ghosted you before you could ghost them first." |
| Only one language across all repos | "Monolingual and proud... comfort zone? Never heard of it." |
| Last push ≥ 90 days ago | "You commit less than your college attendance." |
| Last push ≥ 365 days ago | Title becomes "The Digital Fossil" |
| 0 followers | "Not even your mutuals believe in this repo history." |
| Following ≫ followers | "This is not networking, this is begging." |
| ≥15 repos but ≤10 stars total | "Collecting repos like they're Pokemon — gotta catch 'em all, use none." |
| Every repo has no description | "Mystery box energy, except nobody wants to open the box." |
| Mostly forks, few original repos | "A very elaborate bookmarks folder." |
| High average stars/repo | A rare compliment, grudgingly given |

Because these are independent boolean checks over live API data, two
different usernames produce genuinely different roast cards — the output
varies with the account, it isn't a single canned string. A title,
primary roast, and verdict are also derived from the same signals, and the
selection is deterministically shuffled per-username so a given profile's
roast card is stable across reloads.

## Key concepts demonstrated

- **GitHub REST API** — `GET /users/{username}` and
  `GET /users/{username}/repos`, unauthenticated (works for public data,
  capped at 60 requests/hour per IP)
- **`requests`** — HTTP calls, timeouts, JSON parsing, pagination
- **Flask** — routes, `request.values`, template rendering
- **Procedural generation** — template + data-driven roast logic, gated on
  multiple independent real-world conditions
- **Jinja2** — templated, styled HTML roast card with template inheritance
  (`base.html` → `index.html` / `roast.html` / `error.html`)
- **Graceful error handling** — 404 (user not found), 403 (rate limited),
  and network failures all render a clean in-UI message instead of a stack
  trace

## Run it

Requires Python 3.8+.

```bash
cd ProfilePulse
pip install -r requirements.txt
python app.py
```

Then open **http://localhost:5000** and roast a username (try `octocat`,
`torvalds`, or your own).

## Project structure

```
ProfilePulse/
├── app.py              # Flask routes, GitHub API fetch + error handling
├── roast.py            # Procedural roast generation engine
├── templates/
│   ├── base.html        # Shared layout
│   ├── index.html       # Home page / username form
│   ├── roast.html        # Roast card
│   └── error.html       # Clean error page
├── static/
│   └── style.css        # Roast card styling
├── requirements.txt
└── README.md
```

## Notes / limitations

- Uses unauthenticated GitHub API requests (60/hour rate limit per IP).
  For heavier use, add a personal access token via `Authorization` header
  and an `.env` file (already ignored by `.gitignore`).
- "Last commit" is approximated as the most recent `pushed_at` timestamp
  across the user's public repos, since GitHub's REST API doesn't expose a
  single global "last commit" field without walking commit history per repo.

## Notes

Built as a focused, single-purpose tool - a GitHub profile roaster, nothing more, nothing less.

## Troubleshooting

If something doesn't run as expected, double-check you're using the dependency versions noted above and running the exact commands from the "Run it" section.

## Possible Improvements

- More test coverage
- Better error messages for edge cases
- A cleaner CLI/UI polish pass

## Acknowledgements

Thanks to the open-source libraries this project leans on - see the dependency list above for the full set.

## License

GPLv3 - see [LICENSE](LICENSE) for details.
