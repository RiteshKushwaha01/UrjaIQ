'use client'

import { useEffect, useState } from 'react'

const navigation = [
  { label: 'Home', href: '#home', id: 'home' },
  { label: 'Overview', href: '#overview', id: 'overview' },
  { label: 'Live Monitoring', href: '#monitoring', id: 'monitoring' },
  { label: 'Production', href: '#production', id: 'production' },
  { label: 'Anomaly Detection', href: '#anomalies', id: 'anomalies' },
  { label: 'Energy Optimization', href: '#optimization', id: 'optimization' },
  { label: 'Carbon & Sustainability', href: '#carbon', id: 'carbon' },
  { label: 'AI Copilot', href: '#copilot', id: 'copilot' },
]

type SidebarProps = {
  open?: boolean
  onClose?: () => void
}

export default function Sidebar({ open = false, onClose }: SidebarProps) {
  const [activeId, setActiveId] = useState('home')

  useEffect(() => {
    const sections = navigation
      .map((item) => document.getElementById(item.id))
      .filter((section): section is HTMLElement => Boolean(section))

    if (sections.length === 0) {
      return
    }

    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio)

        if (visible[0]?.target.id) {
          setActiveId(visible[0].target.id)
        }
      },
      {
        rootMargin: '-20% 0px -60% 0px',
        threshold: [0.1, 0.25, 0.5],
      },
    )

    sections.forEach((section) => observer.observe(section))

    return () => observer.disconnect()
  }, [])

  return (
    <>
      <div
        className={`fixed inset-0 z-40 bg-slate-950/70 backdrop-blur-sm transition lg:hidden ${
          open ? 'opacity-100' : 'pointer-events-none opacity-0'
        }`}
        onClick={onClose}
      />

      <aside
        className={`fixed inset-y-0 left-0 z-50 w-72 border-r border-slate-800 bg-slate-950 transition-transform duration-200 lg:sticky lg:top-[65px] lg:z-0 lg:h-[calc(100vh-65px)] lg:w-64 lg:translate-x-0 ${
          open ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex h-full flex-col">
          <div className="flex items-center justify-between border-b border-slate-800 px-5 py-4">
            <div>
              <p className="text-[11px] font-semibold uppercase tracking-[0.16em] text-slate-500">
                Sections
              </p>
              <p className="mt-1 text-sm font-medium text-slate-200">
                Platform navigation
              </p>
            </div>

            <button
              type="button"
              onClick={onClose}
              className="inline-flex h-8 w-8 items-center justify-center rounded-md text-slate-400 hover:bg-slate-900 hover:text-white lg:hidden"
              aria-label="Close navigation"
            >
              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.8"
                className="h-4 w-4"
              >
                <path d="M6 6l12 12M18 6L6 18" strokeLinecap="round" />
              </svg>
            </button>
          </div>

          <nav className="flex-1 overflow-y-auto px-3 py-4">
            <div className="space-y-1">
              {navigation.map((item, index) => {
                const isActive = activeId === item.id

                return (
                  <a
                    key={item.href}
                    href={item.href}
                    onClick={onClose}
                    className={`flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition ${
                      isActive
                        ? 'bg-emerald-500/10 text-emerald-300 ring-1 ring-emerald-500/20'
                        : 'text-slate-400 hover:bg-slate-900 hover:text-white'
                    }`}
                  >
                    <span
                      className={`flex h-6 w-6 shrink-0 items-center justify-center rounded-md text-[11px] ${
                        isActive
                          ? 'bg-emerald-500/20 text-emerald-300'
                          : 'bg-slate-900 text-slate-500'
                      }`}
                    >
                      {String(index + 1).padStart(2, '0')}
                    </span>
                    {item.label}
                  </a>
                )
              })}
            </div>
          </nav>

          <div className="border-t border-slate-800 p-4">
            <p className="text-xs font-medium text-slate-400">UrjaIQ</p>
            <p className="mt-1 text-xs leading-5 text-slate-600">
              Industrial Energy Intelligence
            </p>
          </div>
        </div>
      </aside>
    </>
  )
}
