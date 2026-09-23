'use client'

import { useEffect, useState } from 'react'
import {
  CarbonOverview as CarbonOverviewData,
  getCarbonOverview,
} from '@/lib/api'

export default function CarbonOverview() {
  const [data, setData] = useState<CarbonOverviewData | null>(null)

  useEffect(() => {
    async function loadCarbonData() {
      try {
        const carbonData = await getCarbonOverview()
        setData(carbonData)
      } catch (error) {
        console.error('Failed to load carbon overview:', error)
      }
    }

    loadCarbonData()
  }, [])

  if (!data) {
    return (
      <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
        <p className="text-sm text-slate-400">Loading carbon data...</p>
      </section>
    )
  }

  return (
    <section className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-semibold text-white">
          Carbon & Sustainability
        </h2>

        <p className="mt-1 text-sm text-slate-400">
          Estimated electricity-related emissions based on validated production
          batches.
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid gap-4 md:grid-cols-4">
        <MetricCard
          title="Estimated CO₂e"
          value={`${data.estimated_co2e_kg.toFixed(2)} kg`}
          subtitle="validated batches"
        />

        <MetricCard
          title="Carbon Intensity"
          value={`${data.estimated_co2e_per_good_unit_kg.toFixed(4)} kg`}
          subtitle="CO₂e per good unit"
        />

        <MetricCard
          title="Energy Consumption"
          value={`${data.total_energy_kwh.toFixed(2)} kWh`}
          subtitle="validated batches"
        />

        <MetricCard
          title="Batches Analyzed"
          value={data.batches_analyzed.toString()}
          subtitle={`${data.good_units} good units`}
        />
      </div>

      {/* Methodology */}
      <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
        <h3 className="text-base font-semibold text-white">
          Carbon Calculation
        </h3>

        <div className="mt-4 grid gap-4 md:grid-cols-2">
          <div className="rounded-xl border border-slate-800 bg-slate-950 p-4">
            <p className="text-sm text-slate-400">
              Electricity Emission Factor
            </p>

            <p className="mt-2 text-2xl font-semibold text-white">
              {data.emission_factor_kg_co2e_per_kwh.toFixed(2)}
            </p>

            <p className="mt-1 text-xs text-slate-500">kg CO₂e per kWh</p>
          </div>

          <div className="rounded-xl border border-slate-800 bg-slate-950 p-4">
            <p className="text-sm text-slate-400">Calculation</p>

            <p className="mt-2 text-sm text-slate-300">
              Energy × emission factor = estimated CO₂e
            </p>

            <p className="mt-2 text-xs text-slate-500">
              {data.total_energy_kwh.toFixed(2)} kWh ×{' '}
              {data.emission_factor_kg_co2e_per_kwh.toFixed(2)} kg/kWh
            </p>
          </div>
        </div>

        <p className="mt-5 text-xs text-amber-400">
          Prototype estimate: the emission factor is currently a configurable
          assumption and should be replaced with a documented,
          region-appropriate factor for production use.
        </p>
      </div>
    </section>
  )
}

function MetricCard({
  title,
  value,
  subtitle,
}: {
  title: string
  value: string
  subtitle: string
}) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
      <p className="text-sm text-slate-400">{title}</p>

      <p className="mt-2 text-2xl font-semibold text-white">{value}</p>

      <p className="mt-1 text-xs text-slate-500">{subtitle}</p>
    </div>
  )
}
