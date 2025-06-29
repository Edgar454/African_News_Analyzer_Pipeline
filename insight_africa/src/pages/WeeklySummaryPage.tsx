import ReactMarkdown from 'react-markdown'
import {
  useWeeklySummary,
  useNetworkMetrics,
  useNodeMetrics,
  useWeeklyInsights
} from '../utils/api'

import Header from '../components/Header/RegularHeader'
import InsightsSidebar from '../components/WeeklySummary/InsightSidebar'
import TopicModelTags from '../components/WeeklySummary/TopicTags'
import TopicModelGraph from '../components/WeeklySummary/EmbeddedTopicHTML'
import NetworkGraph from '../components/WeeklySummary/KnowledgeGraphSection'
import NetworkMetrics from '../components/WeeklySummary/NetworkMetricsGrid'
import NodeCentralityTable from '../components/WeeklySummary/NodeCentralityTable'

export default function WeeklySummaryPage() {
  const { data: summary, error: summaryError } = useWeeklySummary()
  const { data: networkMetrics, error: networkError } = useNetworkMetrics()
  const { data: nodeMetrics, error: nodeError } = useNodeMetrics()
  const { data: weeklyInsights, error: insightsError } = useWeeklyInsights()

  // S'il y a une erreur sur n'importe quelle donnée, afficher un message d'erreur global
  if (summaryError || networkError || nodeError || insightsError) {
    return (
      <div className="relative flex size-full min-h-screen flex-col bg-white group/design-root overflow-x-hidden" style={{ fontFamily: 'Newsreader, "Noto Sans", sans-serif' }}>
        <div className="layout-container flex h-full grow flex-col">
          <Header />
          <div className="gap-1 px-6 flex flex-1 justify-center py-5">
            <InsightsSidebar />
            <main className="layout-content-container flex flex-col max-w-[960px] flex-1 p-4 text-red-600 font-bold text-center">
              Error loading summary data.
            </main>
          </div>
        </div>
      </div>
    )
  }

  const isLoading = !summary || !networkMetrics || !nodeMetrics || !weeklyInsights

  return (
    <div className="relative flex size-full min-h-screen flex-col bg-white group/design-root overflow-x-hidden" style={{ fontFamily: 'Newsreader, "Noto Sans", sans-serif' }}>
      <div className="layout-container flex h-full grow flex-col">
        <Header />

        <div className="gap-1 px-6 flex flex-1 justify-center py-5">
          <InsightsSidebar />

          <main className="layout-content-container flex flex-col max-w-[960px] flex-1">
            {/* Titre principal toujours affiché */}
            <div className="flex min-w-72 flex-col gap-3 p-4">
              <p id="weekly-summary" className="text-[#131416] tracking-light text-[32px] font-bold leading-tight">
                Weekly News Summary
              </p>

              {/* Date uniquement si loaded */}
              {!isLoading && summary && (
                <p className="text-[#6b7680] text-sm font-normal leading-normal">
                  Week of {new Date(summary.week_start).toLocaleDateString(undefined, { month: 'long', day: 'numeric', year: 'numeric' })}
                </p>
              )}
            </div>

            {/* Contenu principal */}
            {isLoading ? (
              // Spinner centré pendant le chargement
              <div className="flex justify-center items-center py-20">
                <svg
                  className="animate-spin h-8 w-8 text-gray-600"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  />
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
                  />
                </svg>
              </div>
            ) : (
              <>
                {/* AI Summary */}
                <h3 className="text-[#131416] text-lg font-bold leading-tight tracking-[-0.015em] px-4 pb-2 pt-4">
                  Core News of the week
                </h3>
                <div className="prose prose-sm max-w-none text-[#131416] pb-3 pt-1 px-4">
                  <ReactMarkdown>{summary.summary_text}</ReactMarkdown>
                </div>

                {/* Knowledge Graph */}
                <h3 id="knowledge-graph" className="text-[#131416] text-lg font-bold leading-tight tracking-[-0.015em] px-4 pb-2 pt-4">
                  Knowledge Graph
                </h3>
                <div className="flex px-4 py-3">
                  <NetworkGraph />
                </div>

                {/* Network Metrics */}
                <h3 className="text-[#131416] text-lg font-bold leading-tight tracking-[-0.015em] px-4 pb-2 pt-4">
                  Network Metrics
                </h3>
                <NetworkMetrics metrics={networkMetrics} />

                {/* Node Centrality */}
                <NodeCentralityTable nodeMetrics={nodeMetrics} />

                {/* Topic Model Visualization*/} 
                <h3 id="topic-modeling" className="text-[#131416] text-lg font-bold leading-tight tracking-[-0.015em] px-4 pb-2 pt-4">
                  Topic Model Visualization
                </h3>
                <TopicModelGraph />

                {/* Topic Model Tags */}
                <h3 className="text-[#131416] text-lg font-bold leading-tight tracking-[-0.015em] px-4 pb-2 pt-4">
                  Topic Model Tags
                </h3>
                <TopicModelTags topics={summary.topic_model} />

                {/* Weekly Insights */}
                <h3 id="network-analysis" className="text-[#131416] text-lg font-bold leading-tight tracking-[-0.015em] px-4 pb-2 pt-4">
                  Overall Summary
                </h3>
                <div className="prose prose-sm max-w-none text-[#131416] pb-3 pt-1 px-4">
                  <ReactMarkdown>{weeklyInsights.summary}</ReactMarkdown>
                </div>
              </>
            )}
          </main>
        </div>
      </div>
    </div>
  )
}
