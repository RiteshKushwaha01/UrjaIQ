'use client'

import { useState } from 'react'

import DashboardHeader from '@/components/dashboard/DashboardHeader'
import Footer from '@/components/dashboard/Footer'
import Sidebar from '@/components/dashboard/Sidebar'

export default function DashboardShell({
  children,
}: {
  children: React.ReactNode
}) {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <div className="flex min-h-screen flex-col bg-slate-950 text-slate-100">
      <DashboardHeader onMenuClick={() => setSidebarOpen(true)} />

      <div className="flex min-h-0 flex-1">
        <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} />

        <div className="min-w-0 flex-1">{children}</div>
      </div>

      <Footer />
    </div>
  )
}
