'use client'

import { useEffect, useState } from 'react'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

type Anomaly = {
  timestamp: string
  machine_id: string
  machine_type: string
  power_kw: number
  temperature: number
  vibration: number
  operating_state: string
  anomaly_score: number
}

function formatMachineType(machineType: string) {
  return machineType
    .split('_')
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

export default function AnomalyAlerts() {
  const [anomalies, setAnomalies] = useState<Anomaly[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let isMounted = true

    async function loadAnomalies() {
      try {
        const response = await fetch(
          `${API_BASE_URL}/api/ml/anomalies?limit=5`,
          {
            cache: 'no-store',
          },
        )

        if (!response.ok) {
          throw new Error('Failed to fetch anomaly data')
        }

        const data: Anomaly[] = await response.json()

        if (isMounted) {
          setAnomalies(data)
          setLoading(false)
        }
      } catch (error) {
        console.error('Failed to load anomaly alerts:', error)

        if (isMounted) {
          setLoading(false)
        }
      }
    }

    loadAnomalies()

    const intervalId = setInterval(loadAnomalies, 10000)

    return () => {
      isMounted = false
      clearInterval(intervalId)
    }
  }, [])

  return (
    <section className="mt-8">
      <div className="mb-4">
        <h2 className="text-xl font-semibold text-white">
          AI Anomaly Detection
        </h2>

        <p className="mt-1 text-sm text-slate-400">
          Machine conditions identified as statistically abnormal by the ML
          model.
        </p>
      </div>

      {loading ? (
        <div className="rounded-xl border border-slate-800 bg-slate-900 p-6 text-sm text-slate-400">
          Analyzing machine telemetry...
        </div>
      ) : anomalies.length === 0 ? (
        <div className="rounded-xl border border-emerald-500/20 bg-emerald-500/10 p-6">
          <p className="font-medium text-emerald-400">No anomalies detected</p>
          <p className="mt-1 text-sm text-slate-400">
            Current machine telemetry is within the learned operating patterns.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {anomalies.map((anomaly, index) => (
            <div
              key={`${anomaly.machine_id}-${anomaly.timestamp}-${index}`}
              className="rounded-xl border border-red-500/20 bg-slate-900 p-5"
            >
              <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
                <div>
                  <div className="flex items-center gap-3">
                    <span className="h-2.5 w-2.5 rounded-full bg-red-400" />

                    <h3 className="font-semibold text-white">
                      {anomaly.machine_id}
                    </h3>

                    <span className="rounded-full border border-red-500/20 bg-red-500/10 px-2.5 py-1 text-xs font-medium text-red-400">
                      Anomaly
                    </span>
                  </div>

                  <p className="mt-1 text-sm text-slate-400">
                    {formatMachineType(anomaly.machine_type)}
                  </p>
                </div>

                <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
                  <div>
                    <p className="text-xs text-slate-500">Power</p>
                    <p className="mt-1 text-sm font-medium text-slate-200">
                      {anomaly.power_kw.toFixed(1)} kW
                    </p>
                  </div>

                  <div>
                    <p className="text-xs text-slate-500">Temperature</p>
                    <p className="mt-1 text-sm font-medium text-slate-200">
                      {anomaly.temperature.toFixed(1)}°C
                    </p>
                  </div>

                  <div>
                    <p className="text-xs text-slate-500">Vibration</p>
                    <p className="mt-1 text-sm font-medium text-slate-200">
                      {anomaly.vibration.toFixed(2)}
                    </p>
                  </div>

                  <div>
                    <p className="text-xs text-slate-500">ML Score</p>
                    <p className="mt-1 text-sm font-medium text-red-400">
                      {anomaly.anomaly_score.toFixed(4)}
                    </p>
                  </div>
                </div>
              </div>

              <div className="mt-4 border-t border-slate-800 pt-3">
                <p className="text-xs text-slate-500">
                  Operating state:{' '}
                  <span className="text-slate-300">
                    {anomaly.operating_state}
                  </span>
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  )
}
