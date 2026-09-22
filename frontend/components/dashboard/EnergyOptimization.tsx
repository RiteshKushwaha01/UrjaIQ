'use client'

import { useEffect, useState } from 'react'
import {
  getMachineEnergy,
  getOptimizationBaseline,
  getOptimizationRecommendations,
  getSavingsEstimate,
  MachineEnergy,
  OptimizationBaseline,
  OptimizationRecommendation,
  SavingsEstimate,
} from '@/lib/api'

export default function EnergyOptimization() {
  const [baseline, setBaseline] = useState<OptimizationBaseline | null>(null)

  const [machineEnergy, setMachineEnergy] = useState<MachineEnergy[]>([])

  const [savings, setSavings] = useState<SavingsEstimate | null>(null)

  const [recommendations, setRecommendations] = useState<
    OptimizationRecommendation[]
  >([])

  useEffect(() => {
    async function loadData() {
      try {
        const [baselineData, energyData, savingsData, recommendationData] =
          await Promise.all([
            getOptimizationBaseline(),
            getMachineEnergy(),
            getSavingsEstimate(),
            getOptimizationRecommendations(),
          ])

        setBaseline(baselineData)
        setMachineEnergy(energyData.machines)
        setSavings(savingsData)
        setRecommendations(recommendationData.recommendations)
      } catch (error) {
        console.error('Failed to load optimization data:', error)
      }
    }

    loadData()
  }, [])

  if (!baseline || !savings) {
    return (
      <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
        <p className="text-sm text-slate-400">Loading energy optimization...</p>
      </section>
    )
  }

  return (
    <section className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-semibold text-white">
          Energy Optimization
        </h2>

        <p className="mt-1 text-sm text-slate-400">
          Baseline analysis, optimization scenario, and machine-level energy
          recommendations.
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid gap-4 md:grid-cols-4">
        <MetricCard
          title="Baseline SEC"
          value={`${baseline.average_sec_kwh_per_good_unit.toFixed(4)} kWh`}
          subtitle="per good unit"
        />

        <MetricCard
          title="Optimized SEC"
          value={`${savings.optimized_scenario.estimated_sec_kwh_per_good_unit.toFixed(4)} kWh`}
          subtitle="estimated scenario"
        />

        <MetricCard
          title="SEC Improvement"
          value={`${savings.optimized_scenario.estimated_sec_improvement_percent.toFixed(1)}%`}
          subtitle="estimated"
        />

        <MetricCard
          title="Estimated Saving"
          value={`₹${savings.savings.estimated_cost_saving_inr.toFixed(2)}`}
          subtitle="per analyzed batch"
        />
      </div>

      {/* Machine Energy Distribution */}
      <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
        <h3 className="text-base font-semibold text-white">
          Machine Energy Distribution
        </h3>

        <div className="mt-5 space-y-4">
          {machineEnergy.map((machine) => (
            <div key={machine.machine_id}>
              <div className="mb-2 flex items-center justify-between">
                <span className="text-sm text-slate-300">
                  {machine.machine_id}
                </span>

                <span className="text-sm font-medium text-white">
                  {machine.energy_share_percent.toFixed(1)}%
                </span>
              </div>

              <div className="h-2 overflow-hidden rounded-full bg-slate-800">
                <div
                  className="h-full rounded-full bg-emerald-500"
                  style={{
                    width: `${Math.min(machine.energy_share_percent, 100)}%`,
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Estimated Savings */}
      <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
        <h3 className="text-base font-semibold text-white">
          Estimated Savings
        </h3>

        <div className="mt-4 grid gap-4 md:grid-cols-3">
          <MetricCard
            title="Energy Saving"
            value={`${savings.savings.estimated_energy_saving_kwh.toFixed(4)} kWh`}
            subtitle="estimated per batch"
          />

          <MetricCard
            title="Cost Saving"
            value={`₹${savings.savings.estimated_cost_saving_inr.toFixed(2)}`}
            subtitle={`at ₹${savings.assumptions.electricity_tariff_inr_per_kwh}/kWh`}
          />

          <MetricCard
            title="Baseline Energy"
            value={`${savings.baseline.average_energy_kwh.toFixed(4)} kWh`}
            subtitle="per analyzed batch"
          />
        </div>

        <p className="mt-4 text-xs text-amber-400">
          Savings are simulated estimates based on an assumed{' '}
          {savings.assumptions.estimated_reduction_percent}% reduction scenario.
        </p>
      </div>

      {/* Recommendations */}
      <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
        <h3 className="text-base font-semibold text-white">
          Optimization Recommendations
        </h3>

        <div className="mt-4 space-y-3">
          {recommendations.map((recommendation) => (
            <div
              key={recommendation.machine_id}
              className="rounded-xl border border-slate-800 bg-slate-950 p-4"
            >
              <div className="flex items-center justify-between gap-4">
                <h4 className="font-medium text-white">
                  {recommendation.title}
                </h4>

                <span className="rounded-full border border-slate-700 px-2.5 py-1 text-xs text-slate-300">
                  {recommendation.priority}
                </span>
              </div>

              <p className="mt-2 text-sm leading-6 text-slate-400">
                {recommendation.description}
              </p>

              <p className="mt-2 text-xs text-slate-500">
                Energy share: {recommendation.energy_share_percent.toFixed(1)}%
              </p>
            </div>
          ))}
        </div>
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
