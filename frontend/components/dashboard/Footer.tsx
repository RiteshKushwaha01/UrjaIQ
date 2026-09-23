export default function Footer() {
  return (
    <footer className="border-t border-slate-800 bg-slate-950">
      <div className="px-6 py-8 lg:px-10">
        <div className="grid gap-8 md:grid-cols-3">
          <div>
            <div className="flex items-center gap-3">
              <div className="flex h-8 w-8 items-center justify-center rounded-full bg-emerald-500 text-xs font-bold text-slate-950">
                UQ
              </div>
              <h2 className="text-base font-semibold text-white">UrjaIQ</h2>
            </div>

            <p className="mt-3 max-w-sm text-sm leading-6 text-slate-400">
              AI-powered industrial energy and process intelligence for smarter,
              more efficient manufacturing.
            </p>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-white">Platform</h3>

            <ul className="mt-3 space-y-2 text-sm text-slate-400">
              <li>
                <a href="#overview" className="transition hover:text-white">
                  Factory Overview
                </a>
              </li>
              <li>
                <a href="#monitoring" className="transition hover:text-white">
                  Live Monitoring
                </a>
              </li>
              <li>
                <a href="#optimization" className="transition hover:text-white">
                  Energy Optimization
                </a>
              </li>
              <li>
                <a href="#carbon" className="transition hover:text-white">
                  Carbon & Sustainability
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-white">About UrjaIQ</h3>

            <p className="mt-3 text-sm leading-6 text-slate-400">
              UrjaIQ combines real-time industrial telemetry, analytics, machine
              intelligence, optimization, and carbon insights to help
              manufacturing teams make data-driven decisions.
            </p>
          </div>
        </div>

        <div className="mt-8 border-t border-slate-800 pt-5">
          <div className="flex flex-col justify-between gap-2 text-xs text-slate-500 sm:flex-row">
            <p>© 2026 UrjaIQ. Industrial Energy Intelligence Platform.</p>
            <p>Built for smart and sustainable manufacturing.</p>
          </div>
        </div>
      </div>
    </footer>
  )
}
