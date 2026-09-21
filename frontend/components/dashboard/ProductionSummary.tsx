'use client'

import { useEffect, useState } from 'react'

import { MachineTelemetry } from '@/lib/api'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function ProductionSummary() {
  const [data, setData] = useState<MachineTelemetry | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let isMounted = true

    async function loadProduction() {
      try {
        const response = await fetch(
          `${API_BASE_URL}/api/telemetry/machine/Furnace-01/latest`,
          {
            cache: 'no-store',
          },
        )

        if (!response.ok) {
          throw new Error('Failed to fetch production data')
        }

        const telemetry: MachineTelemetry = await response.json()

        if (isMounted) {
          setData(telemetry)
          setLoading(false)
        }
      } catch (error) {
        console.error('Failed to load production data:', error)

        if (isMounted) {
          setLoading(false)
        }
      }
    }

    loadProduction()

    const intervalId = setInterval(loadProduction, 2000)

    return () => {
      isMounted = false
      clearInterval(intervalId)
    }
  }, [])

  if (loading) {
    return (
      <section className="mt-8 rounded-xl border border-slate-800 bg-slate-900 p-5">
        <p className="text-sm text-slate-400">Loading production data...</p>
      </section>
    )
  }

  if (!data) {
    return null
  }

  const qualityRate =
    data.production_units > 0
      ? (data.good_units / data.production_units) * 100
      : 0

  return (
    <section className="mt-8">
      <div className="mb-4">
        <h2 className="text-xl font-semibold text-white">
          Production & Quality
        </h2>

        <p className="mt-1 text-sm text-slate-400">
          Current production performance from the furnace process.
        </p>
      </div>

      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <div className="rounded-xl border border-slate-800 bg-slate-900 p-5">
          <p className="text-sm text-slate-400">Production Units</p>

          <p className="mt-2 text-2xl font-bold text-white">
            {data.production_units}
          </p>
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-900 p-5">
          <p className="text-sm text-slate-400">Good Units</p>

          <p className="mt-2 text-2xl font-bold text-white">
            {data.good_units}
          </p>
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-900 p-5">
          <p className="text-sm text-slate-400">Rejected Units</p>

          <p className="mt-2 text-2xl font-bold text-white">
            {data.rejected_units}
          </p>
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-900 p-5">
          <p className="text-sm text-slate-400">Quality Rate</p>

          <p className="mt-2 text-2xl font-bold text-white">
            {qualityRate.toFixed(1)}%
          </p>
        </div>
      </div>
    </section>
  )
}
