import React from 'react'
import { useKnowledgeGraphJSON } from '../../utils/api'
import ForceGraph2D from 'react-force-graph-2d'

export default function NetworkGraph() {
  const { data, error } = useKnowledgeGraphJSON()

  if (error) return <p>Error loading network graph.</p>
  if (!data) return <p>Loading network graph...</p>

  // The data format is node-link JSON for NetworkX, 
  // typically { nodes: [...], links: [...] }

  return (
    <div className="w-full max-w-full h-[500px] overflow-hidden rounded-md border border-gray-300 shadow">
  <ForceGraph2D
    graphData={data}
    nodeLabel="id"
    nodeAutoColorBy="group"
    linkDirectionalArrowLength={4}
    linkDirectionalArrowRelPos={1}
    linkCurvature={0.25}
    width={window.innerWidth > 960 ? 900 : window.innerWidth - 100} // optional
    height={450}
  />
</div>

  )
}
