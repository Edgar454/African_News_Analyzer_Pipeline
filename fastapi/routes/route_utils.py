import os
from dotenv import load_dotenv
from mistralai import Mistral

import json
from fastapi import HTTPException

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")
model = "open-mistral-nemo"

client = Mistral(api_key=api_key)

def relative_change(old: float, new: float) -> float:
    if old == 0:
        return 0.0
    return abs(new - old) / old


async def provide_weekly_summary(db_pool):
        async with db_pool.acquire() as conn:
            # Weekly summary (text + topics)
            summary_row = await conn.fetchrow("""
                SELECT week_start, week_end, summary_text, topic_model
                FROM weekly_summaries
                ORDER BY week_start DESC
                LIMIT 1;
            """)

            if not summary_row:
                raise HTTPException(status_code=404, detail="No weekly summary found.")

            week_start = summary_row["week_start"]
            week_end = summary_row["week_end"]
            summary_text = summary_row["summary_text"]
            topic_model = json.loads(summary_row["topic_model"])

            # Network-level metrics
            net_row = await conn.fetchrow("""
                SELECT num_nodes, num_edges, avg_path_length, clustering_coefficient, num_communities
                FROM network_metrics
                WHERE week_start = $1
                LIMIT 1;
            """, week_start)

            if not net_row:
                raise HTTPException(status_code=404, detail="No network metrics found.")

            network_metrics = dict(net_row)

            # Node-level metrics
            node_row = await conn.fetchrow("""
                SELECT metrics
                FROM node_metrics
                WHERE week_start = $1
                LIMIT 1;
            """, week_start)

            if not node_row:
                raise HTTPException(status_code=404, detail="No node metrics found.")

            node_metrics = json.loads(node_row["metrics"])

        # 🧠 Compose prompt
        prompt = f"""
You are a data journalist creating a weekly report on news trends from {week_start} to {week_end}.

You are given:
1. A raw summary of major events
2. A topic model output
3. Network-level statistics about the connections between entities
4. Node-level metrics showing individual entity importance

Write a clean, readable summary of the week. Highlight:
- What themes dominated the week
- What structural insights the network tells us
- Which entities were central or influential
- Any notable patterns

--- RAW SUMMARY TEXT ---
{summary_text}

--- TOPIC MODEL OUTPUT ---
{json.dumps(topic_model, indent=2)}

--- NETWORK METRICS ---
{json.dumps(network_metrics, indent=2)}

--- NODE METRICS (PageRank, centrality, etc.) ---
{json.dumps(node_metrics, indent=2)}
"""

        
        response = client.chat.complete(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert in summarizing news and social network data for weekly reports."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=800
        )

        return response.choices[0].message.content





async def compare_two_weeks(db_pool):
        async with db_pool.acquire() as conn:
            # Get last 2 network summaries
            net_rows = await conn.fetch("""
                SELECT id, week_start, num_nodes, num_edges, avg_path_length,
                       clustering_coefficient, num_communities
                FROM network_metrics
                ORDER BY week_start DESC
                LIMIT 2;
            """)

            # Get last 2 node-level metrics
            node_rows = await conn.fetch("""
                SELECT week_start, metrics
                FROM node_metrics
                ORDER BY week_start DESC
                LIMIT 2;
            """)

        if len(net_rows) < 2 or len(node_rows) < 2:
            raise HTTPException(status_code=404, detail="Not enough weekly data to compare.")

        # Convert DB rows to usable Python dicts
        net1, net2 = [dict(r) for r in net_rows]
        node1, node2 = [dict(r) for r in node_rows]

        net1["week_start"] = net1["week_start"].isoformat()
        net2["week_start"] = net2["week_start"].isoformat()

        node1["metrics"] = json.loads(node1["metrics"])
        node2["metrics"] = json.loads(node2["metrics"])

        # calculate aggregation metrics
        number_change = relative_change(net1["num_nodes"], net2["num_nodes"])
        density_change = relative_change(net1["clustering_coefficient"], net2["clustering_coefficient"])

        # Compose prompt
        prompt = f"""
You are a network analyst comparing two weekly network snapshots derived from news data.

--- WEEK 1 ({net1['week_start']}) ---
Network summary:
{json.dumps(net1, indent=2)}

Node-level metrics (PageRank, centrality, etc.):
{json.dumps(node1["metrics"], indent=2)}

--- WEEK 2 ({net2['week_start']}) ---
Network summary:
{json.dumps(net2, indent=2)}

Node-level metrics (PageRank, centrality, etc.):
{json.dumps(node2["metrics"], indent=2)}

Please write a clear and engaging summary for a general audience interested in news trends. Your summary should:

- Begin with an introduction explaining the purpose of the comparison and what the network represents (e.g., connections among news topics, sources, or actors).
- Describe major changes in the network structure in simple terms, connecting these changes to possible shifts in news themes, topics, or collaborations.
- Discuss key actors or entities that became more or less influential, relating their importance to real-world events or trends.
- Highlight any emerging or disappearing news topics or groups, and what these might imply.
- Avoid heavy technical jargon; if network terms are used, explain them briefly and clearly.
- Conclude with insights on how these network changes reflect evolving news narratives or information flows.

Keep the summary concise, informative, and accessible to readers without a technical background in network analysis.
"""



        # Call OpenAI
        response = client.chat.complete(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert in social network analysis."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1500
        )

        summary = response.choices[0].message.content

        return summary , net2["num_nodes"], net2["clustering_coefficient"], number_change, density_change
