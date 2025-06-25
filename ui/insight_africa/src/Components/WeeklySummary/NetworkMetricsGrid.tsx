import React from 'react';

interface NetworkMetricsProps {
  metrics: {
    num_nodes: number;
    avg_path_length: number | null;
    clustering_coefficient: number;
  };
}

export default function NetworkMetrics({ metrics }: NetworkMetricsProps) {
  const { num_nodes, avg_path_length, clustering_coefficient } = metrics;

  return (
    <section className="flex flex-wrap gap-4 p-4">
      <MetricCard title="Nodes" value={num_nodes.toString()} />
      <MetricCard title="Avg. Path Length" value={(avg_path_length ?? 'N/A').toString()} />
      <MetricCard title="Clustering Coefficient" value={clustering_coefficient.toFixed(2)} />
    </section>
  );
}


function MetricCard({ title, value }: { title: string; value: string }) {
  return (
    <div className="flex min-w-[158px] flex-1 flex-col gap-2 rounded-xl p-6 border border-[#dee0e3]">
      <p className="text-[#131416] text-base font-medium leading-normal">{title}</p>
      <p className="text-[#131416] tracking-light text-2xl font-bold leading-tight">{value}</p>
    </div>
  );
}