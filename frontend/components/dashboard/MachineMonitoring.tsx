'use client'

import { useEffect, useState } from 'react'
import { getLatestMachineTelemetry, MachineTelemetry } from '@/lib/api'

const machineIds = ['Furnace-01', 'Compressor-01', 'Motor-01', 'Cooling-01']

function getStatusStyle(status: string) {
  if (status === 'warning') {
    return 'border-amber-500/20 bg-amber-500/10 text-amber-400'
  }

  if (status === 'degraded') {
    return 'border-red-500/20 bg-red-500/10 text-red-400'
  }

  return 'border-emerald-500/20 bg-emerald-500/10 text-emerald-400'
}

function formatMachineType(machineType: string) {
  return machineType
    .split('_')
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

export default function MachineMonitoring() {
  const [telemetry, setTelemetry] = useState<Record<string, MachineTelemetry>>(
    {},
  )
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function loadTelemetry() {
      try {
        setError(null)

        const results = await Promise.all(
          machineIds.map(async (machineId) => {
            const data = await getLatestMachineTelemetry(machineId)

            return [machineId, data] as const
          }),
        )

        setTelemetry(Object.fromEntries(results))
      } catch (err) {
        console.error('Failed to load machine telemetry:', err)
        setError('Unable to load live machine data.')
      } finally {
        setLoading(false)
      }
    }

    loadTelemetry()
  }, [])

  return (
    <section className="mt-8">
      <div className="mb-4">
        <h2 className="text-xl font-semibold text-white">Machine Monitoring</h2>

        <p className="mt-1 text-sm text-slate-400">
          Live operating conditions across the factory floor.
        </p>
      </div>

      {loading && (
        <div className="rounded-xl border border-slate-800 bg-slate-900 p-6 text-sm text-slate-400">
          Loading live machine telemetry...
        </div>
      )}

      {error && (
        <div className="rounded-xl border border-red-500/20 bg-red-500/10 p-6 text-sm text-red-400">
          {error}
        </div>
      )}

      {!loading && !error && (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
          {machineIds.map((machineId) => {
            const machine = telemetry[machineId]

            if (!machine) {
              return null
            }

            return (
              <div
                key={machine.machine_id}
                className="rounded-xl border border-slate-800 bg-slate-900 p-5"
              >
                <div className="flex items-start justify-between">
                  <div>
                    <h3 className="font-semibold text-white">
                      {machine.machine_id}
                    </h3>

                    <p className="mt-1 text-sm text-slate-400">
                      {formatMachineType(machine.machine_type)}
                    </p>
                  </div>

                  <span
                    className={`rounded-full border px-2.5 py-1 text-xs font-medium ${getStatusStyle(
                      machine.operating_state,
                    )}`}
                  >
                    {machine.operating_state}
                  </span>
                </div>

                <div className="mt-5 grid grid-cols-2 gap-4 sm:grid-cols-4">
                  <div>
                    <p className="text-xs text-slate-500">Power</p>
                    <p className="mt-1 text-sm font-medium text-slate-200">
                      {machine.power_kw.toFixed(1)} kW
                    </p>
                  </div>

                  <div>
                    <p className="text-xs text-slate-500">Temperature</p>
                    <p className="mt-1 text-sm font-medium text-slate-200">
                      {machine.temperature.toFixed(1)}°C
                    </p>
                  </div>

                  <div>
                    <p className="text-xs text-slate-500">Vibration</p>
                    <p className="mt-1 text-sm font-medium text-slate-200">
                      {machine.vibration.toFixed(2)}
                    </p>
                  </div>

                  <div>
                    <p className="text-xs text-slate-500">Good Units</p>
                    <p className="mt-1 text-sm font-medium text-slate-200">
                      {machine.good_units}
                    </p>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </section>
  )
}
