export default function RoastCard() {
  return (
    <div className="w-full max-w-md rounded-2xl border border-white/10 bg-gradient-to-b from-[#15151f] to-[#0d0d13] p-6 shadow-[0_0_0_1px_rgba(255,255,255,0.02),0_20px_60px_-20px_rgba(249,115,22,0.25)]">
      {/* Header */}
      <div className="flex items-center gap-3">
        <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-orange-500 to-pink-600 text-lg font-bold text-white">
          SU
        </div>
        <div className="min-w-0">
          <p className="truncate font-semibold text-white">@someuser</p>
          <p className="truncate text-sm font-medium text-orange-400">
            The Ghost Committer
          </p>
        </div>
      </div>

      {/* Stats */}
      <div className="mt-5 grid grid-cols-2 gap-2 text-sm">
        <div className="rounded-lg bg-white/5 px-3 py-2">
          <span className="text-neutral-400">📦 Repos</span>
          <p className="font-semibold text-white">23</p>
        </div>
        <div className="rounded-lg bg-white/5 px-3 py-2">
          <span className="text-neutral-400">⭐ Total stars</span>
          <p className="font-semibold text-white">4 (yikes)</p>
        </div>
        <div className="col-span-2 rounded-lg bg-white/5 px-3 py-2">
          <span className="text-neutral-400">🗓️ Last commit</span>
          <p className="font-semibold text-white">4 months ago</p>
        </div>
      </div>

      {/* Roast */}
      <div className="mt-4 rounded-lg border border-orange-500/20 bg-orange-500/10 p-3">
        <p className="text-xs font-semibold uppercase tracking-wide text-orange-400">
          🔥 Roast
        </p>
        <p className="mt-1 text-sm leading-snug text-neutral-100">
          &ldquo;23 repos, 4 stars, and the audacity to have a bio.&rdquo;
        </p>
      </div>

      {/* Verdict */}
      <div className="mt-3 rounded-lg border border-white/10 bg-white/[0.03] p-3">
        <p className="text-xs font-semibold uppercase tracking-wide text-neutral-400">
          💀 Verdict
        </p>
        <p className="mt-1 text-sm leading-snug text-neutral-200">
          Collecting repos like they&rsquo;re Pok&eacute;mon &mdash; gotta
          catch &rsquo;em all, use none.
        </p>
      </div>
    </div>
  );
}
