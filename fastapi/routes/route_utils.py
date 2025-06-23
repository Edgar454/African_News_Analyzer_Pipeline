import os
from dotenv import load_dotenv
import mistralai

import json
from fastapi import HTTPException

api_key = os.getenv("MISTRAL_API_KEY",)
model = "open-mistral-nemo"

client = Mistral(api_key=api_key)




async def provide_weekly_summary(db_pool):
    try:
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

    except Exception as e:
        print(f"Error generating full weekly summary: {e}")
        raise HTTPException(status_code=500, detail="Failed to provide weekly summary.")



async def compare_two_weeks(db_pool):
    try:
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
        node1["metrics"] = json.loads(node1["metrics"])
        node2["metrics"] = json.loads(node2["metrics"])

        # Compose prompt
        prompt = f"""
You are a network analyst. Compare the following two weekly network snapshots.

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

Write a detailed analyst-style summary highlighting:
- Changes in network structure (communities, density, paths)
- Changes in node importance (PageRank, etc.)
- New or disappearing key actors
- Any other interesting patterns
"""

        # Call OpenAI
        response = client.chat.complete(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert in social network analysis."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=700
        )

        summary = response.choices[0].message.content

        return summary

    
