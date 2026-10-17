import RoastCard from "./components/RoastCard";

const techBadges = [
  "Python",
  "Flask",
  "Jinja2",
  "GitHub REST API",
  "requests",
  "Procedural Generation",
];

const triggers = [
  {
    pattern: "Repos exist but total stars ≤ 5",
    line: "“23 repos, 4 stars, and the audacity to have a bio.”",
  },
  {
    pattern: "No bio set on the profile",
    line: "“Even your repos ghosted you before you could ghost them first.”",
  },
  {
    pattern: "Last push ≥ 90 days ago",
    line: "“You commit less than your college attendance.”",
  },
  {
    pattern: "≥ 15 repos but ≤ 10 total stars",
    line: "“Collecting repos like they're Pokemon — gotta catch 'em all, use none.”",
  },
];

export default function Home() {
  return (
    <div className="flex flex-1 flex-col">
      {/* Ambient glow */}
      <div
        aria-hidden
        className="pointer-events-none fixed inset-0 -z-10 bg-[radial-gradient(ellipse_60%_50%_at_50%_-10%,rgba(249,115,22,0.18),transparent)]"
      />

      {/* Hero */}
      <header className="mx-auto w-full max-w-5xl px-6 pt-20 pb-12 text-center sm:pt-28">
        <p className="mb-4 inline-block rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs font-medium tracking-wide text-neutral-400">
          GitHub Profile Roaster
        </p>
        <h1 className="text-balance text-4xl font-bold tracking-tight text-white sm:text-6xl">
          ProfilePulse
        </h1>
        <p className="mx-auto mt-5 max-w-2xl text-balance text-lg text-neutral-400 sm:text-xl">
          Type any GitHub username. Get back a{" "}
          <span className="text-orange-400">roast card</span> built from
          their real, public stats — not a canned insult.
        </p>
        <p className="mx-auto mt-6 max-w-2xl text-balance text-sm leading-relaxed text-neutral-500">
          ProfilePulse pulls a GitHub profile and every public repo straight
          from the GitHub REST API, then runs the numbers through a
          procedural roast engine that only fires lines whose trigger
          condition is actually true for that account. Real repo counts,
          real stars, real activity gaps — turned into commentary that
          changes with the profile, not a script.
        </p>

        {/* Live roaster: submits straight to the Flask app on this host */}
        <form
          action="/roast"
          method="get"
          className="mx-auto mt-10 flex w-full max-w-md flex-col gap-3 sm:flex-row"
        >
          <input
            name="username"
            required
            placeholder="GitHub username, e.g. torvalds"
            autoComplete="off"
            className="flex-1 rounded-lg border border-white/10 bg-white/5 px-4 py-3 text-white placeholder:text-neutral-500 focus:border-orange-400 focus:outline-none"
          />
          <button
            type="submit"
            className="rounded-lg bg-orange-500 px-6 py-3 font-semibold text-white transition hover:bg-orange-400"
          >
            Roast them
          </button>
        </form>
        <p className="mt-3 text-xs text-neutral-500">
          Live — runs against the real GitHub API.
        </p>
      </header>

      {/* X Factor */}
      <section className="mx-auto w-full max-w-5xl px-6 py-12">
        <div className="mb-8 text-center">
          <h2 className="text-sm font-semibold uppercase tracking-widest text-orange-400">
            The X Factor
          </h2>
          <p className="mx-auto mt-3 max-w-2xl text-balance text-neutral-300">
            Every roast line is gated on an independent, real data condition
            evaluated against the GitHub API response. Two usernames almost
            never produce the same roast card, because the output is
            computed from the account, not picked from a fixed list of
            insults.
          </p>
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          {triggers.map((t) => (
            <div
              key={t.pattern}
              className="rounded-xl border border-white/10 bg-white/[0.03] p-5"
            >
              <p className="text-xs font-semibold uppercase tracking-wide text-neutral-500">
                Trigger
              </p>
              <p className="mt-1 font-mono text-sm text-neutral-300">
                {t.pattern}
              </p>
              <div className="mt-3 border-t border-white/10 pt-3">
                <p className="text-xs font-semibold uppercase tracking-wide text-orange-400">
                  Roast line
                </p>
                <p className="mt-1 text-sm text-neutral-200">{t.line}</p>
              </div>
            </div>
          ))}
        </div>
        <p className="mt-6 text-center text-sm text-neutral-500">
          Plus more triggers for monolingual repos, stale activity, follower
          imbalance, missing descriptions, fork-heavy profiles, and even a
          grudging compliment for genuinely high average stars per repo.
        </p>
      </section>

      {/* Sample output */}
      <section className="mx-auto w-full max-w-5xl px-6 py-12">
        <div className="mb-8 text-center">
          <h2 className="text-sm font-semibold uppercase tracking-widest text-orange-400">
            Sample Output
          </h2>
          <p className="mx-auto mt-3 max-w-2xl text-balance text-neutral-300">
            What a roast card actually looks like once the engine runs
            against a real profile.
          </p>
        </div>
        <div className="flex justify-center">
          <RoastCard />
        </div>
      </section>

      {/* Tech badges */}
      <section className="mx-auto w-full max-w-5xl px-6 py-12">
        <div className="mb-6 text-center">
          <h2 className="text-sm font-semibold uppercase tracking-widest text-orange-400">
            Key Concepts
          </h2>
        </div>
        <div className="flex flex-wrap justify-center gap-2">
          {techBadges.map((b) => (
            <span
              key={b}
              className="rounded-full border border-white/10 bg-white/5 px-4 py-1.5 text-sm text-neutral-300"
            >
              {b}
            </span>
          ))}
        </div>
      </section>

      {/* Run it */}
      <section className="mx-auto w-full max-w-3xl px-6 py-16">
        <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-8">
          <h2 className="text-sm font-semibold uppercase tracking-widest text-orange-400">
            Run It Locally
          </h2>
          <p className="mt-3 text-sm text-neutral-400">
            The roaster above is live on this site. To run your own copy, start
            the Flask app and open{" "}
            <code className="rounded bg-white/10 px-1.5 py-0.5 font-mono text-neutral-200">
              localhost:5000
            </code>
            .
          </p>
          <pre className="mt-4 overflow-x-auto rounded-lg bg-black/60 p-4 font-mono text-sm text-neutral-200">
            <code>{`cd ProfilePulse
pip install flask requests
python app.py
# then open http://localhost:5000`}</code>
          </pre>
          <p className="mt-4 text-xs text-neutral-500">
            Requires Python 3.8+. Set GITHUB_TOKEN to raise the GitHub API
            limit from 60 to 5,000 requests/hour.
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="mx-auto w-full max-w-5xl px-6 pb-16 pt-4 text-center text-xs text-neutral-600">
        <p>ProfilePulse &middot; Python &amp; Flask &middot; Licensed under GPLv3</p>
      </footer>
    </div>
  );
}
