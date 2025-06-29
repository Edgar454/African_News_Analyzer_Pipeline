import { useState } from 'react';
import type { NodeMetrics } from '../../utils/api'


interface NodeData {
  node: string;
  pagerank: number;
  centrality: number;
}

interface NodeCentralityTableProps {
  nodeMetrics: NodeMetrics;
}

export default function NodeCentralityTable({ nodeMetrics }: NodeCentralityTableProps) {
  const { page_rank, betweenness_centrality } = nodeMetrics.metrics;
  const [sortBy, setSortBy] = useState<'pagerank' | 'centrality'>('pagerank');

  const nodeMap: Record<string, NodeData> = {};

  betweenness_centrality.forEach(([node, value]) => {
    nodeMap[node] = { node, centrality: value, pagerank: 0 };
  });

  page_rank.forEach(([node, value]) => {
    if (!nodeMap[node]) nodeMap[node] = { node, centrality: 0, pagerank: value };
    else nodeMap[node].pagerank = value;
  });

  const sortedNodes = Object.values(nodeMap).sort((a, b) => b[sortBy] - a[sortBy]);

  return (
    <section className="px-4 py-3">
      <div className="flex justify-between items-center pb-2">
        <h3 className="text-[#131416] text-lg font-bold leading-tight tracking-[-0.015em]">
          Node Centrality
        </h3>
        <div className="flex items-center gap-2">
          <label htmlFor="sort-select" className="text-sm text-[#6b7680]">Sort by:</label>
          <select
            id="sort-select"
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as 'pagerank' | 'centrality')}
            className="text-sm px-2 py-1 border border-gray-300 rounded-md"
          >
            <option value="pagerank">PageRank</option>
            <option value="centrality">Betweenness Centrality</option>
          </select>
        </div>
      </div>

      <div className="flex overflow-hidden rounded-xl border border-[#dee0e3] bg-white">
        <table className="flex-1">
          <thead>
            <tr className="bg-white">
              <th className="px-4 py-3 text-left text-[#131416] text-sm font-medium leading-normal">Node</th>
              <th className="px-4 py-3 text-left text-[#131416] text-sm font-medium leading-normal">Betweenness Centrality</th>
              <th className="px-4 py-3 text-left text-[#131416] text-sm font-medium leading-normal">PageRank</th>
            </tr>
          </thead>
          <tbody>
            {sortedNodes.map((n, idx) => (
              <tr key={idx} className="border-t border-t-[#dee0e3]">
                <td className="px-4 py-2 text-[#131416] text-sm font-normal leading-normal">{n.node}</td>
                <td className="px-4 py-2 text-[#6b7680] text-sm font-normal leading-normal">{n.centrality.toFixed(2)}</td>
                <td className="px-4 py-2 text-[#6b7680] text-sm font-normal leading-normal">{n.pagerank.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
