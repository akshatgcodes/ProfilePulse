"""
ProfilePulse — a GitHub profile roaster.

Flask web app: type a GitHub username, fetch their public data via the
GitHub REST API (no auth required for public data / low rate limits),
and render a procedurally-generated "roast card" mixing real stats with
savage-but-accurate commentary.

Run:
    pip install flask requests
    python app.py
    open http://localhost:5000
"""

from flask import Flask, render_template, request
import requests

from roast import build_roast_context

app = Flask(__name__)

GITHUB_API = "https://api.github.com"
REQUEST_TIMEOUT = 8  # seconds
HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "ProfilePulse-Roast-App",
}


class GitHubLookupError(Exception):
    """Raised when we can't get usable data back from the GitHub API."""

    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def fetch_github_data(username):
    """
    Fetch a user's public profile + repos from the GitHub REST API.
    Raises GitHubLookupError with a human-readable message on any failure
    (not found, rate limited, network error, etc.) so routes never leak
    a stack trace to the UI.
    """
    try:
        user_resp = requests.get(
            f"{GITHUB_API}/users/{username}", headers=HEADERS, timeout=REQUEST_TIMEOUT
        )
    except requests.exceptions.RequestException:
        raise GitHubLookupError(
            "Couldn't reach GitHub right now. Check your connection and try again."
        )

    if user_resp.status_code == 404:
        raise GitHubLookupError(f'No GitHub user found for "{username}".', 404)

    if user_resp.status_code == 403:
        raise GitHubLookupError(
            "GitHub API rate limit hit. Unauthenticated requests are capped "
            "at 60/hour — wait a bit and try again.",
            403,
        )

    if user_resp.status_code != 200:
        raise GitHubLookupError(
            f"GitHub API returned an unexpected error (status "
            f"{user_resp.status_code}). Try again in a moment.",
            user_resp.status_code,
        )

    user = user_resp.json()

    repos = []
    page = 1
    try:
        while True:
            repos_resp = requests.get(
                f"{GITHUB_API}/users/{username}/repos",
                headers=HEADERS,
                params={"per_page": 100, "page": page, "type": "owner"},
                timeout=REQUEST_TIMEOUT,
            )
            if repos_resp.status_code == 403:
                raise GitHubLookupError(
                    "GitHub API rate limit hit while fetching repos. "
                    "Wait a bit and try again.",
                    403,
                )
            if repos_resp.status_code != 200:
                break
            batch = repos_resp.json()
            if not isinstance(batch, list) or not batch:
                break
            repos.extend(batch)
            if len(batch) < 100 or page >= 5:  # cap at 500 repos, plenty
                break
            page += 1
    except requests.exceptions.RequestException:
        raise GitHubLookupError(
            "Couldn't fetch repo data from GitHub. Check your connection and try again."
        )

    return user, repos


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/roast", methods=["GET", "POST"])
def roast():
    username = (request.values.get("username") or "").strip().lstrip("@")

    if not username:
        return render_template(
            "error.html", message="Enter a GitHub username to roast."
        )

    try:
        user, repos = fetch_github_data(username)
    except GitHubLookupError as exc:
        return render_template("error.html", message=exc.message)

    context = build_roast_context(user, repos)

    return render_template(
        "roast.html",
        user=user,
        username=user.get("login", username),
        roast=context,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
