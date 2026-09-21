const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export type MachineTelemetry = {
  id: number
  timestamp: string
  batch_id: string
  machine_id: string
  machine_type: string
  power_kw: number
  energy_kwh: number
  temperature: number
  vibration: number
  voltage: number
  current: number
  operating_state: string
  production_units: number
  good_units: number
  rejected_units: number
}

export async function getLatestMachineTelemetry(
  machineId: string,
): Promise<MachineTelemetry> {
  const response = await fetch(
    `${API_BASE_URL}/api/telemetry/machine/${encodeURIComponent(
      machineId,
    )}/latest`,
    {
      cache: 'no-store',
    },
  )

  if (!response.ok) {
    throw new Error(
      `Failed to fetch telemetry for ${machineId}: ${response.status}`,
    )
  }

  return response.json()
}
