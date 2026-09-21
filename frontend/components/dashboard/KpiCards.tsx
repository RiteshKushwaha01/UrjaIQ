'use client'

import { useEffect, useState } from 'react'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

type FactoryOverview = {
  total_energy_kwh: number
  peak_power_kw: number
  production_units: number
  good_units: number
  rejected_units: number
  quality_rate: number
  specific_energy_kwh_per_good_unit: number
}

export default function KpiCards() {
  const [data, setData] = useState<FactoryOverview | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let isMounted = true

    async function loadOverview() {
      try {
        const response = await fetch(`${API_BASE_URL}/api/analytics/overview`, {
          cache: 'no-store',
        })

        if (!response.ok) {
          throw new Error('Failed to fetch factory analytics')
        }

        const overview: FactoryOverview = await response.json()

        if (isMounted) {
          setData(overview)
          setLoading(false)
        }
      } catch (error) {
        console.error('Failed to load factory analytics:', error)

        if (isMounted) {
          setLoading(false)
        }
      }
    }

    loadOverview()

    const intervalId = setInterval(loadOverview, 2000)

    return () => {
      isMounted = false
      clearInterval(intervalId)
    }
  }, [])

  const kpis = data
    ? [
        {
          label: 'Total Energy',
          value: `${data.total_energy_kwh.toFixed(2)} kWh`,
        },
        {
          label: 'Peak Demand',
          value: `${data.peak_power_kw.toFixed(1)} kW`,
        },
        {
          label: 'Specific Energy',
          value: `${data.specific_energy_kwh_per_good_unit.toFixed(
            2,
          )} kWh/unit`,
        },
        {
          label: 'Quality Rate',
          value: `${data.quality_rate.toFixed(1)}%`,
        },
      ]
    : []

  return (
    <section className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
      {loading
        ? Array.from({ length: 4 }).map((_, index) => (
            <div
              key={index}
              className="rounded-xl border border-slate-800 bg-slate-900 p-5"
            >
              <p className="text-sm text-slate-400">Loading...</p>

              <div className="mt-3 h-8 w-32 animate-pulse rounded bg-slate-800" />
            </div>
          ))
        : kpis.map((kpi) => (
            <div
              key={kpi.label}
              className="rounded-xl border border-slate-800 bg-slate-900 p-5"
            >
              <p className="text-sm text-slate-400">{kpi.label}</p>

              <p className="mt-2 text-2xl font-bold tracking-tight text-white">
                {kpi.value}
              </p>

              <p className="mt-2 text-xs text-slate-500">
                Live factory analytics
              </p>
            </div>
          ))}
    </section>
  )
}
