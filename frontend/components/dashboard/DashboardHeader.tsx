'use client'

type DashboardHeaderProps = {
  onMenuClick?: () => void
}

export default function DashboardHeader({ onMenuClick }: DashboardHeaderProps) {
  return (
    <header className="sticky top-0 z-40 border-b border-slate-800/80 bg-slate-950/90 backdrop-blur-md">
      <div className="flex items-center justify-between gap-4 px-4 py-3 lg:px-6">
        <div className="flex min-w-0 items-center gap-3">
          <button
            type="button"
            onClick={onMenuClick}
            className="inline-flex h-10 w-10 items-center justify-center rounded-lg border border-slate-800 text-slate-300 transition hover:bg-slate-900 hover:text-white lg:hidden"
            aria-label="Open navigation"
          >
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.8"
              className="h-5 w-5"
            >
              <path d="M4 7h16M4 12h16M4 17h16" strokeLinecap="round" />
            </svg>
          </button>

          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-500 text-sm font-bold tracking-tight text-slate-950 shadow-[0_0_24px_rgba(16,185,129,0.35)]">
            UQ
          </div>

          <div className="min-w-0">
            <h1 className="truncate text-lg font-semibold tracking-tight text-white">
              UrjaIQ
            </h1>
            <p className="hidden truncate text-xs text-slate-400 sm:block">
              Industrial Energy & Process Optimization
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="hidden items-center gap-2 rounded-full border border-slate-800 bg-slate-900/70 px-3 py-1.5 text-xs text-slate-400 md:flex">
            <span>Plant</span>
            <span className="font-medium text-slate-200">Line 01</span>
          </div>

          <div className="flex items-center gap-2 rounded-full border border-emerald-500/20 bg-emerald-500/10 px-3 py-1.5">
            <span className="relative flex h-2 w-2">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-60" />
              <span className="relative inline-flex h-2 w-2 rounded-full bg-emerald-400" />
            </span>
            <span className="text-xs font-medium text-emerald-400 sm:text-sm">
              System Online
            </span>
          </div>
        </div>
      </div>
    </header>
  )
}
