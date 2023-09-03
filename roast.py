"""
roast.py — Procedural roast generation for ProfilePulse.

Takes real GitHub stats (repo count, stars, languages, activity, followers,
bio, etc.) and turns them into savage-but-accurate one-liners. Each roast
line is gated on a specific, real data condition — nothing here is a single
canned string. Multiple triggers can fire; we pick the sharpest ones and
compute a title + verdict + overall roast.
"""

from datetime import datetime, timezone
import random


def _days_since(iso_timestamp):
    """Return days elapsed since an ISO8601 GitHub timestamp, or None."""
    if not iso_timestamp:
        return None
    try:
        dt = datetime.strptime(iso_timestamp, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc
        )
    except ValueError:
        return None
    return (datetime.now(timezone.utc) - dt).days


def _humanize_days(days):
    if days is None:
        return "unknown"
    if days < 1:
        return "today"
    if days < 30:
        return f"{days} day{'s' if days != 1 else ''} ago"
    months = days // 30
    if months < 12:
        return f"{months} month{'s' if months != 1 else ''} ago"
    years = days // 365
    return f"{years} year{'s' if years != 1 else ''} ago"


def build_roast_context(user, repos):
    """
    Compute derived stats from raw GitHub API payloads and generate a
    list of roast lines + a title + a verdict.

    user: dict from GET /users/{username}
    repos: list of dicts from GET /users/{username}/repos
    """
    repo_count = user.get("public_repos", 0) or 0
    follower_count = user.get("followers", 0) or 0
    following_count = user.get("following", 0) or 0
    bio = (user.get("bio") or "").strip()
    has_bio = bool(bio)

    total_stars = sum(r.get("stargazers_count", 0) or 0 for r in repos)
    forked_repos = [r for r in repos if r.get("fork")]
    original_repos = [r for r in repos if not r.get("fork")]
    repos_without_description = [
        r for r in repos if not (r.get("description") or "").strip()
    ]

    languages = {}
    for r in repos:
        lang = r.get("language")
        if lang:
            languages[lang] = languages.get(lang, 0) + 1
    distinct_languages = sorted(languages, key=languages.get, reverse=True)

    # Most recent push across all repos (best proxy for "last commit").
    push_dates = [r.get("pushed_at") for r in repos if r.get("pushed_at")]
    most_recent_push = max(push_dates) if push_dates else None
    days_since_last_push = _days_since(most_recent_push)

    avg_stars = (total_stars / repo_count) if repo_count else 0
    has_no_repos = repo_count == 0
    fork_ratio = (len(forked_repos) / repo_count) if repo_count else 0

    roasts = []

    # --- Trigger conditions (each gated on real, independent data) ---

    if has_no_repos:
        roasts.append(
            "Zero public repos. Either a stealth billionaire founder or "
            "GitHub is just where you go to look at other people's code."
        )

    if not has_no_repos and total_stars == 0:
        roasts.append(
            f"{repo_count} repo{'s' if repo_count != 1 else ''}, 0 stars. "
            "Even your own alt account didn't star these."
        )
    elif not has_no_repos and total_stars <= 5:
        roasts.append(
            f"{repo_count} repos, {total_stars} total star"
            f"{'s' if total_stars != 1 else ''} across all of them (yikes)."
        )

    if not has_bio:
        roasts.append(
            "No bio. Even your repos ghosted you before you could ghost "
            "them first."
        )
    elif has_bio and total_stars <= 5 and not has_no_repos:
        roasts.append(
            f'{repo_count} repos, {total_stars} stars, and the audacity '
            f'to have a bio that says "{bio[:60]}".'
        )

    if len(distinct_languages) == 1:
        roasts.append(
            f"Monolingual and proud: every single repo is {distinct_languages[0]}. "
            "Comfort zone? Never heard of it."
        )
    elif len(distinct_languages) == 0 and not has_no_repos:
        roasts.append(
            "GitHub can't even detect a primary language in your repos. "
            "That's not versatility, that's an identity crisis."
        )

    if days_since_last_push is not None and days_since_last_push >= 365:
        roasts.append(
            f"Last commit {_humanize_days(days_since_last_push)}. "
            "This account is basically a digital fossil."
        )
    elif days_since_last_push is not None and days_since_last_push >= 90:
        roasts.append(
            f"Last commit {_humanize_days(days_since_last_push)} — you commit "
            "less than your college attendance."
        )

    if follower_count == 0:
        roasts.append(
            "Zero followers. Not even your mutuals believe in this repo history."
        )
    elif following_count > follower_count * 10 and following_count >= 20:
        roasts.append(
            f"Following {following_count} people but only {follower_count} "
            "follow back. This is not networking, this is begging."
        )

    if repo_count >= 15 and total_stars <= 10:
        roasts.append(
            "Collecting repos like they're Pokemon — gotta catch 'em all, "
            "use none."
        )

    if not has_no_repos and len(repos_without_description) == repo_count:
        roasts.append(
            "Not a single repo has a description. Mystery box energy, "
            "except nobody wants to open the box."
        )

    if not has_no_repos and fork_ratio >= 0.6 and len(original_repos) <= 3:
        roasts.append(
            "Mostly forks, barely any original work. A GitHub profile "
            "that's really just a very elaborate bookmarks folder."
        )

    if avg_stars >= 50:
        roasts.append(
            f"Okay actually {avg_stars:.0f} stars per repo on average — "
            "grudging respect. Don't let it go to your head."
        )

    # Fallback if somehow nothing triggered (very well-rounded profile).
    if not roasts:
        roasts.append(
            "Suspiciously well-rounded profile. Either genuinely impressive "
            "or you know exactly what recruiters are looking for."
        )

    random.Random(user.get("login", "")).shuffle(roasts)
    primary_roast = roasts[0]

    # --- Title generation ---
    if has_no_repos:
        title = "The Ghost"
    elif days_since_last_push is not None and days_since_last_push >= 365:
        title = "The Digital Fossil"
    elif total_stars == 0 and repo_count >= 5:
        title = "The Ghost Committer"
    elif len(distinct_languages) == 1 and repo_count >= 3:
        title = f"The {distinct_languages[0]} Loyalist"
    elif fork_ratio >= 0.6 and repo_count >= 5:
        title = "The Serial Forker"
    elif repo_count >= 15 and total_stars <= 10:
        title = "The Repo Hoarder"
    elif avg_stars >= 50:
        title = "The Low-Key Legend"
    elif follower_count == 0:
        title = "The Lone Wolf"
    else:
        title = "The Mysterious Committer"

    # --- Verdict generation ---
    verdict_pool = [
        "Ship something before your next commit becomes a museum exhibit.",
        "A GitHub graveyard with a green square once every full moon.",
        "The bio says 'building cool stuff.' The commit history disagrees.",
        "Somewhere between 'aspiring developer' and 'developer, aspiring.'",
        "Technically active. Legally active. Spiritually retired.",
        "Impressive stat spread, questionable follow-up energy.",
    ]
    if avg_stars >= 50:
        verdict = "Alright, alright — the stars don't lie. Certified not-mid."
    elif has_no_repos:
        verdict = "A profile so empty it loops back around to mysterious."
    else:
        verdict = random.Random(user.get("login", "") + "v").choice(verdict_pool)

    return {
        "title": title,
        "primary_roast": primary_roast,
        "all_roasts": roasts,
        "verdict": verdict,
        "stats": {
            "repo_count": repo_count,
            "total_stars": total_stars,
            "follower_count": follower_count,
            "following_count": following_count,
            "has_bio": has_bio,
            "bio": bio,
            "distinct_languages": distinct_languages,
            "days_since_last_push": days_since_last_push,
            "last_push_human": _humanize_days(days_since_last_push),
            "avg_stars": round(avg_stars, 1),
            "fork_ratio": round(fork_ratio * 100),
        },
    }
