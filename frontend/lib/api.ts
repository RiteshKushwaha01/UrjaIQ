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

export interface OptimizationBaseline {
  batches_analyzed: number
  average_energy_kwh: number
  average_production_units: number
  average_good_units: number
  average_rejected_units: number
  average_quality_rate: number
  average_sec_kwh_per_good_unit: number
}

export interface MachineEnergy {
  machine_id: string
  machine_type: string
  total_energy_kwh: number
  average_power_kw: number
  peak_power_kw: number
  energy_share_percent: number
}

export interface MachineEnergyResponse {
  total_factory_energy_kwh: number
  machines: MachineEnergy[]
}

export interface OptimizationRecommendation {
  machine_id: string
  machine_type: string
  priority: string
  type: string
  title: string
  description: string
  energy_kwh: number
  energy_share_percent: number
}

export interface OptimizationRecommendationsResponse {
  recommendations: OptimizationRecommendation[]
  count: number
}

export interface SavingsEstimate {
  assumptions: {
    estimated_reduction_percent: number
    electricity_tariff_inr_per_kwh: number
  }

  baseline: {
    average_energy_kwh: number
    average_good_units: number
    sec_kwh_per_good_unit: number
  }

  optimized_scenario: {
    estimated_energy_kwh: number
    estimated_sec_kwh_per_good_unit: number
    estimated_sec_improvement_percent: number
  }

  savings: {
    estimated_energy_saving_kwh: number
    estimated_cost_saving_inr: number
  }
}

export async function getOptimizationBaseline(): Promise<OptimizationBaseline> {
  const response = await fetch(`${API_BASE_URL}/api/optimization/baseline`, {
    cache: 'no-store',
  })

  if (!response.ok) {
    throw new Error(`Failed to fetch optimization baseline: ${response.status}`)
  }

  return response.json()
}

export async function getMachineEnergy(): Promise<MachineEnergyResponse> {
  const response = await fetch(
    `${API_BASE_URL}/api/optimization/machine-energy`,
    {
      cache: 'no-store',
    },
  )

  if (!response.ok) {
    throw new Error(`Failed to fetch machine energy: ${response.status}`)
  }

  return response.json()
}

export async function getOptimizationRecommendations(): Promise<OptimizationRecommendationsResponse> {
  const response = await fetch(
    `${API_BASE_URL}/api/optimization/recommendations`,
    {
      cache: 'no-store',
    },
  )

  if (!response.ok) {
    throw new Error(
      `Failed to fetch optimization recommendations: ${response.status}`,
    )
  }

  return response.json()
}

export async function getSavingsEstimate(): Promise<SavingsEstimate> {
  const response = await fetch(`${API_BASE_URL}/api/optimization/savings`, {
    cache: 'no-store',
  })

  if (!response.ok) {
    throw new Error(`Failed to fetch savings estimate: ${response.status}`)
  }

  return response.json()
}

export interface CarbonOverview {
  batches_analyzed: number
  total_energy_kwh: number
  emission_factor_kg_co2e_per_kwh: number
  estimated_co2e_kg: number
  good_units: number
  estimated_co2e_per_good_unit_kg: number
}

export async function getCarbonOverview(): Promise<CarbonOverview> {
  const response = await fetch(`${API_BASE_URL}/api/carbon/overview`, {
    cache: 'no-store',
  })

  if (!response.ok) {
    throw new Error(`Failed to fetch carbon overview: ${response.status}`)
  }

  return response.json()
}