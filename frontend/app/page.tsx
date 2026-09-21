import DashboardHeader from '@/components/dashboard/DashboardHeader'
import KpiCards from '@/components/dashboard/KpiCards'
import MachineMonitoring from '@/components/dashboard/MachineMonitoring'

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-950">
      <DashboardHeader />

      <section className="mx-auto max-w-7xl px-6 py-8">
        <div className="mb-6">
          <h2 className="text-xl font-semibold text-white">Factory Overview</h2>

          <p className="mt-2 text-sm text-slate-400">
            Real-time energy, production, machine health, and process
            intelligence.
          </p>
        </div>

        <KpiCards />

        <MachineMonitoring />
      </section>
    </main>
  )
}
