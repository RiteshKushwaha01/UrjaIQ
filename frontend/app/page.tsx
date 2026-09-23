import DashboardShell from '@/components/dashboard/DashboardShell'

import EnergyTrendChart from '@/components/dashboard/EnergyTrendChart'
import KpiCards from '@/components/dashboard/KpiCards'
import MachineMonitoring from '@/components/dashboard/MachineMonitoring'
import ProductionSummary from '@/components/dashboard/ProductionSummary'
import AnomalyAlerts from '@/components/dashboard/AnomalyAlerts'
import EnergyOptimization from '@/components/dashboard/EnergyOptimization'
import CarbonOverview from '@/components/dashboard/CarbonOverview'
import AICopilot from '@/components/dashboard/AICopilot'

export default function Home() {
  return (
    <DashboardShell>
      <section
        id="home"
        className="border-b border-slate-800 bg-[radial-gradient(circle_at_top_left,rgba(16,185,129,0.12),transparent_28%),linear-gradient(180deg,#020617_0%,#020617_100%)] px-6 py-12 lg:px-10"
      >
        <div className="mx-auto max-w-7xl">
          <p className="text-sm font-medium text-emerald-400">
            Industrial Energy Intelligence
          </p>

          <h2 className="mt-3 text-3xl font-bold tracking-tight text-white md:text-4xl">
            Smarter Energy. Better Manufacturing.
          </h2>

          <p className="mt-4 max-w-3xl text-base leading-7 text-slate-400">
            UrjaIQ helps manufacturing teams monitor energy, understand machine
            behavior, improve process efficiency, detect anomalies, and measure
            sustainability performance from one intelligent platform.
          </p>

          <div className="mt-8 grid gap-4 md:grid-cols-3">
            <InfoCard
              title="Sense"
              description="Capture real-time machine, energy, and production telemetry."
            />
            <InfoCard
              title="Understand"
              description="Turn industrial data into operational and energy insights."
            />
            <InfoCard
              title="Optimize"
              description="Identify opportunities to reduce energy intensity while protecting output and quality."
            />
          </div>
        </div>
      </section>

      <div className="mx-auto max-w-7xl space-y-12 px-6 py-10 lg:px-10">
        <section id="overview" className="scroll-mt-24">
          <div className="mb-6">
            <h2 className="text-xl font-semibold text-white">
              Factory Overview
            </h2>
            <p className="mt-2 text-sm text-slate-400">
              Real-time energy, production, machine health, and process
              intelligence.
            </p>
          </div>

          <KpiCards />
        </section>

        <section id="monitoring" className="scroll-mt-24">
          <MachineMonitoring />
        </section>

        <section id="production" className="scroll-mt-24 space-y-6">
          <ProductionSummary />
          <EnergyTrendChart />
        </section>

        <section id="anomalies" className="scroll-mt-24">
          <AnomalyAlerts />
        </section>

        <section id="optimization" className="scroll-mt-24">
          <EnergyOptimization />
        </section>

        <section id="carbon" className="scroll-mt-24">
          <CarbonOverview />
        </section>

        <AICopilot />
      </div>
    </DashboardShell>
  )
}

function InfoCard({
  title,
  description,
}: {
  title: string
  description: string
}) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-5 shadow-[inset_0_1px_0_rgba(255,255,255,0.04)]">
      <h3 className="text-base font-semibold text-white">{title}</h3>
      <p className="mt-2 text-sm leading-6 text-slate-400">{description}</p>
    </div>
  )
}
