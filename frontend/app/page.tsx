import DashboardHeader from '@/components/dashboard/DashboardHeader'
import EnergyTrendChart from '@/components/dashboard/EnergyTrendChart'
import KpiCards from '@/components/dashboard/KpiCards'
import MachineMonitoring from '@/components/dashboard/MachineMonitoring'
import ProductionSummary from '@/components/dashboard/ProductionSummary'
import AnomalyAlerts from '@/components/dashboard/AnomalyAlerts'
import EnergyOptimization from '@/components/dashboard/EnergyOptimization'

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

        <AnomalyAlerts />

        <EnergyOptimization />

        <EnergyTrendChart />

        <ProductionSummary />
      </section>
    </main>
  )
}
