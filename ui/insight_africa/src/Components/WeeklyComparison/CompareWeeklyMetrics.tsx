// components/WeeklyComparison/CompareWeeklyMetrics.tsx
import React from 'react';

interface CompareProps {
  num_nodes: number;
  clustering_coefficient: number;
  number_change: number;
  density_change: number;
}

function formatChange(value: number) {
  const percent = (value * 100).toFixed(1) + '%';
  return {
    text: (value >= 0 ? '+' : '-') + percent,
    className: value >= 0 ? 'text-[#078838]' : 'text-[#e73908]'
  };
}

export default function CompareWeeklyMetrics({ num_nodes, clustering_coefficient, number_change, density_change }: CompareProps) {
  const numberDelta = formatChange(number_change);
  const densityDelta = formatChange(density_change);

  return (
    <>
      <h2 className="text-[#111518] text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">Key Metrics</h2>
      <div className="flex flex-wrap gap-4 p-4">
        <MetricCard title="Key Entities" value={num_nodes.toString()} delta={numberDelta} />
        <MetricCard title="Network Density" value={clustering_coefficient.toFixed(2)} delta={densityDelta} />
      </div>
    </>
  );
}

function MetricCard({ title, value, delta }: { title: string; value: string; delta: { text: string; className: string } }) {
  return (
    <div className="flex min-w-[158px] flex-1 flex-col gap-2 rounded-xl p-6 border border-[#dce1e5]">
      <p className="text-[#111518] text-base font-medium leading-normal">{title}</p>
      <p className="text-[#111518] tracking-light text-2xl font-bold leading-tight">{value}</p>
      <p className={`text-base font-medium leading-normal ${delta.className}`}>{delta.text}</p>
    </div>
  );
}
