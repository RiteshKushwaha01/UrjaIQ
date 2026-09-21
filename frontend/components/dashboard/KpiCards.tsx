const kpis = [
  {
    label: 'Total Energy',
    value: '1,284 kWh',
    change: '+4.2%',
  },
  {
    label: 'Peak Demand',
    value: '286 kW',
    change: '-3.8%',
  },
  {
    label: 'Specific Energy',
    value: '18.6 kWh/unit',
    change: '-6.4%',
  },
  {
    label: 'Quality Rate',
    value: '96.8%',
    change: '+1.7%',
  },
]

export default function KpiCards() {
  return (
    <section className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
      {kpis.map((kpi) => (
        <div
          key={kpi.label}
          className="rounded-xl border border-slate-800 bg-slate-900 p-5"
        >
          <p className="text-sm text-slate-400">{kpi.label}</p>

          <p className="mt-2 text-2xl font-bold tracking-tight text-white">
            {kpi.value}
          </p>

          <p className="mt-2 text-sm text-emerald-400">
            {kpi.change} vs previous period
          </p>
        </div>
      ))}
    </section>
  )
}
