import os
import json
import datetime
import logging
from dotenv import load_dotenv
from pathlib import Path
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse,HTMLResponse
from pydantic import BaseModel
from typing import List, Dict, Any , Optional
from routes.route_utils import compare_two_weeks , provide_weekly_summary

# Setup
load_dotenv()
OUTPUT_PATH = Path(os.getenv("OUTPUT_DIR"))
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()

# Pydantic Models
class NewsItem(BaseModel):
    id: int
    title: str
    link: str
    description: str
    content: str
    published_date: datetime.datetime
    tags: List[str]
    category: str

class Topic(BaseModel):
    terms: List[str]
    topic: str
    weights: List[float]

class Summary(BaseModel):
    id: int
    week_start: datetime.datetime
    week_end: datetime.datetime
    summary_text: str
    topic_model: List[Topic]

class NetworkMetrics(BaseModel):
    id: int
    week_start: datetime.datetime
    num_nodes: int
    num_edges: int
    avg_path_length: Optional[float]
    clustering_coefficient: float
    num_communities: int

class NodeMetrics(BaseModel):
    id: int
    week_start: datetime.datetime
    metrics: Dict[str, Any]

# Endpoints
@router.get("/get_news/", response_model=List[NewsItem])
async def get_news(request: Request):
    try:
        db_pool = request.app.state.db_pool
        async with db_pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT id, title, link, description, content, published_date, tags, category
                FROM news
                ORDER BY published_date DESC
                LIMIT 100;
            """)
        return [dict(row) for row in rows]
    except Exception as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch news items.")

@router.get("/get_weekly_summary/", response_model=Summary)
async def get_weekly_summary_db(request: Request):
    try:
        db_pool = request.app.state.db_pool
        async with db_pool.acquire() as conn:
            row = await conn.fetchrow("""
                SELECT id, week_start, week_end, summary_text, topic_model
                FROM weekly_summaries
                ORDER BY week_start DESC
                LIMIT 1;
            """)
        if row is None:
            raise HTTPException(status_code=404, detail="No summary found.")

        row_dict = dict(row)
        row_dict["topic_model"] = json.loads(row_dict["topic_model"])
        return row_dict
    except Exception as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch the weekly summary.")

@router.get("/get_weekly_summary_visualization/topic_html")
async def get_topic_html():
    topic_viz_path = OUTPUT_PATH / "graphs" / "topics_visualization" / "lda_visualization.html"
    if not topic_viz_path.exists():
        raise HTTPException(status_code=404, detail="Topic visualization file not found.")

    with open(topic_viz_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@router.get("/get_weekly_summary_visualization/knowledge_graph")
async def get_knowledge_graph():
    knowledge_graph_path = OUTPUT_PATH / "graphs" / "knowledge_visualization" / "knowledge_graph.json"
    if not knowledge_graph_path.exists():
        raise HTTPException(status_code=404, detail="Knowledge graph file not found.")

    with open(knowledge_graph_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return JSONResponse(content=data)

@router.get("/get_weekly_networks_metrics/", response_model=NetworkMetrics)
async def get_weekly_networks_metrics(request: Request):
    try:
        db_pool = request.app.state.db_pool
        async with db_pool.acquire() as conn:
            row = await conn.fetchrow("""
                SELECT id, week_start, num_nodes, num_edges, avg_path_length,
                       clustering_coefficient, num_communities
                FROM network_metrics
                ORDER BY week_start DESC
                LIMIT 1;
            """)
        if row is None:
            raise HTTPException(status_code=404, detail="No metrics found.")
        return dict(row)
    except Exception as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch the network metrics.")

@router.get("/get_weekly_node_metrics/", response_model=NodeMetrics)
async def get_weekly_node_metrics(request: Request):
    try:
        db_pool = request.app.state.db_pool
        async with db_pool.acquire() as conn:
            row = await conn.fetchrow("""
                SELECT id, week_start, metrics
                FROM node_metrics
                ORDER BY week_start DESC
                LIMIT 1;
            """)
        if row is None:
            raise HTTPException(status_code=404, detail="No metrics found.")
        row_dict = dict(row)
        row_dict["metrics"] = json.loads(row_dict["metrics"])
        return row_dict
    except Exception as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch the weekly node metrics.")

@router.get("/get_weekly_summary_insights/")
async def get_weekly_summary_insights(request: Request):
    try:
        db_pool = request.app.state.db_pool
        summary  = await provide_weekly_summary(db_pool)

        return {"summary": summary}

    except Exception as e:
        logger.error(f"Error during insight generation: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate weekly summary insights.")


@router.get("/compare_two_weeks/")
async def compare_two_weeks_route(request: Request):
    try:
        db_pool = request.app.state.db_pool
        summary , num_nodes, clustering_coefficient, number_change, density_change = await compare_two_weeks(db_pool)

        return {"summary": summary, "num_nodes": num_nodes, "clustering_coefficient": clustering_coefficient, "number_change": number_change, "density_change": density_change}

    except Exception as e:
        logger.error(f"Error during comparison: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate weekly comparison.")
