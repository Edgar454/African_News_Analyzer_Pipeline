// utils/api.ts
import useSWR from 'swr'

const API_BASE = '/api';


const fetcher = (url: string) => fetch(url).then(res => {
  if (!res.ok) throw new Error(`Error fetching ${url}: ${res.statusText}`)
  return res.json()
})

// Types (you can extract them separately if needed)
export interface NewsItem {
  id: number
  title: string
  link: string
  description: string
  content: string
  published_date: string
  tags: string[]
  category: string
  source: string
}

export interface Topic {
  topic: string
  terms: string[]
  weights: number[]
}

export interface Summary {
  id: number
  week_start: string
  week_end: string
  summary_text: string
  topic_model: Topic[]
}

export interface NetworkMetrics {
  id: number
  week_start: string
  num_nodes: number
  num_edges: number
  avg_path_length: number | null
  clustering_coefficient: number
  num_communities: number
}

export interface NodeMetrics {
  id: number;
  week_start: string;
  metrics: {
    degree_centrality: [string, number][];
    betweenness_centrality: [string, number][];
    closeness_centrality: [string, number][];
    page_rank: [string, number][];
  };
}

export interface Comparison {
  summary: string
  num_nodes: number
  clustering_coefficient: number
  number_change: number
  density_change: number
}

// --- Hooks for each route ---

export function useNews() {
  return useSWR<NewsItem[]>(`${API_BASE}/get_news/`, fetcher)
}

export function useWeeklySummary() {
  return useSWR<Summary>(`${API_BASE}/get_weekly_summary/`, fetcher)
}

export function useWeeklyTopicHTML() {
  return `${API_BASE}/get_weekly_summary_visualization/topic_html`
}

export function useKnowledgeGraphJSON() {
  return useSWR(`${API_BASE}/get_weekly_summary_visualization/knowledge_graph`, fetcher);
}


export function useNetworkMetrics() {
  return useSWR<NetworkMetrics>(`${API_BASE}/get_weekly_networks_metrics/`, fetcher)
}

export function useNodeMetrics() {
  return useSWR<NodeMetrics>(`${API_BASE}/get_weekly_node_metrics/`, fetcher)
}

export function useWeeklyInsights() {
  return useSWR<{ summary: string }>(`${API_BASE}/get_weekly_summary_insights/`, fetcher)
}

export function useComparison() {
  return useSWR<Comparison>(`${API_BASE}/compare_two_weeks/`, fetcher)
}
