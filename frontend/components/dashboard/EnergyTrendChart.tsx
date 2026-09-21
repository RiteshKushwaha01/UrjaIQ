'use client'

import { useEffect, useState } from 'react'
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

import { MachineTelemetry } from '@/lib/api'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const machineIds = ['Furnace-01', 'Compressor-01', 'Motor-01', 'Cooling-01']

type ChartPoint = {
  time: string
  [key: string]: string | number
}

export default function EnergyTrendChart() {
  const [data, setData] = useState<ChartPoint[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let isMounted = true

    async function loadTelemetry() {
      try {
        const response = await fetch(
          `${API_BASE_URL}/api/telemetry/recent?limit=40`,
          {
            cache: 'no-store',
          },
        )

        if (!response.ok) {
          throw new Error('Failed to fetch recent telemetry')
        }

        const telemetry: MachineTelemetry[] = await response.json()

        const points: ChartPoint[] = telemetry.reverse().map((item) => ({
          time: new Date(item.timestamp).toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
          }),
          [item.machine_id]: Number(item.power_kw.toFixed(1)),
        }))

        if (isMounted) {
          setData(points)
          setLoading(false)
        }
      } catch (error) {
        console.error('Failed to load energy trend:', error)

        if (isMounted) {
          setLoading(false)
        }
      }
    }

    loadTelemetry()

    const intervalId = setInterval(loadTelemetry, 2000)

    return () => {
      isMounted = false
      clearInterval(intervalId)
    }
  }, [])

  return (
    <section className="mt-8 rounded-xl border border-slate-800 bg-slate-900 p-5">
      <div className="mb-5">
        <h2 className="text-xl font-semibold text-white">Energy Consumption</h2>

        <p className="mt-1 text-sm text-slate-400">
          Live machine power consumption over time.
        </p>
      </div>

      {loading ? (
        <div className="flex h-80 items-center justify-center text-sm text-slate-400">
          Loading energy data...
        </div>
      ) : (
        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />

              <XAxis
                dataKey="time"
                tick={{ fill: '#94a3b8', fontSize: 12 }}
                tickLine={false}
                axisLine={false}
              />

              <YAxis
                unit=" kW"
                tick={{ fill: '#94a3b8', fontSize: 12 }}
                tickLine={false}
                axisLine={false}
              />

              <Tooltip
                contentStyle={{
                  backgroundColor: '#0f172a',
                  border: '1px solid #334155',
                  borderRadius: '8px',
                  color: '#fff',
                }}
              />

              {machineIds.map((machineId) => (
                <Line
                  key={machineId}
                  type="monotone"
                  dataKey={machineId}
                  dot={false}
                  strokeWidth={2}
                  connectNulls
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </section>
  )
}
