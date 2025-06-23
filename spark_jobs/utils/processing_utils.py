import os
import json
import pickle
import logging
import datetime
import pandas as pd
import networkx as nx
from utils.graph_helpers import (
    split_text_into_chunks ,documents2DataFrame, df2Graph, graph2Df,post_process_concepts,
    contextual_proximity,aggregate_df,build_graph_from_df ,find_communities,color_graph,write_graph_to_json , compute_graph_metrics
)
from utils.graph_helpers import (classify_in_batches , split_text_into_chunks)
from utils.topic_modeling_helpers import create_dictionary_and_corpus , process_text ,extract_topics,visualize_topics
from utils.prompts import CLASSIFICATION_PROMPT , SUMMARY_PROMPT , generate_completion

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def perform_classification(df: pd.DataFrame) -> pd.DataFrame:
    """
    Classify a list of texts into predefined categories using a classification prompt.
    
    Args:
        texts (list): A list of text descriptions to classify.

    Returns:
        pd.DataFrame: A DataFrame containing the original texts and their corresponding categories.
    """
    logger.info(f"Starting Classification ...")
    categories = classify_in_batches(df, system_prompt=CLASSIFICATION_PROMPT)
    df["category"] = categories
    logger.info(f"Classification ended successfuly")
    return df


def perform_summary(df: pd.DataFrame) -> str:
    """
    Summarize a list of texts into key points using a summary prompt.
    
    Args:
        df (pd.DataFrame): A DataFrame containing the texts to summarize.

    Returns:
        str: A summary of the original texts.
    """
    logger.info(f"Starting Summarization ...")
    complete_texts = "\n----------------\n".join(df["content"].tolist())
    summary = generate_completion(system_prompt="", user_prompt=SUMMARY_PROMPT.format(text=complete_texts))
    logger.info(f"Summarization ended successfuly")

    return summary


def perform_topic_modeling(df: pd.DataFrame, num_topics: int = 5) -> tuple:
    """
    Perform topic modeling on a list of texts using LDA.
    
    Args:
        df (pd.DataFrame): A DataFrame containing the texts to analyze.
        num_topics (int): The number of topics to extract.

    Returns:
        tuple: A tuple containing the dictionary and corpus used for topic modeling.
    """
    texts = df["content"].apply(process_text).tolist()
    topics_data , vectorizer, lda , doc_term_matrix = extract_topics(texts, num_topics=num_topics)

    # Generate visualization of topics
    OUTPUT_DIR = os.environ.get("OUTPUT_DIR","data/graphs/topics_visualization")
    TOPIC_VIZ_PATH = OUTPUT_DIR+"/graphs/topics_visualization"
    os.makedirs(TOPIC_VIZ_PATH, exist_ok=True)

    visualize_topics(lda, vectorizer, doc_term_matrix, TOPIC_VIZ_PATH)
    logger.info(f"Topic Modeling Ended successfully. Graph saved at {TOPIC_VIZ_PATH}/lda_visualization.html")

    return topics_data , vectorizer, lda , doc_term_matrix



def build_and_save_knowledge_graph(df: pd.DataFrame) -> nx.Graph:
    """
    Build and persist a knowledge graph from textual content.

    This function extracts concepts from the given DataFrame, builds a contextual knowledge graph,
    detects communities, colors the nodes, and saves both a .gpickle representation and graph stats.

    Args:
        df (pd.DataFrame): A DataFrame containing textual news content.

    Returns:
        nx.Graph: A NetworkX graph object representing the knowledge graph.
    """

    logger.info("Starting knowledge graph construction...")

    # Step 1: Preprocess text and extract initial concept relationships
    logger.info("Starting dataframe preprocessing")
    documents = split_text_into_chunks(df)
    documents_df = documents2DataFrame(documents)
    concepts_list = df2Graph(documents_df)
    logger.info("Dataframe preprocessing ended")
    

    # Step 2: Convert to edge DataFrame and clean concept labels
    logger.info("Starting concepts extraction")
    concept_edges_df = graph2Df(concepts_list)
    concept_edges_df = post_process_concepts(concept_edges_df)
    logger.info("Concepts extraction ended")

    # Step 3: Add contextual proximity relationships between concepts
    proximity_edges_df = contextual_proximity(concept_edges_df)

    # Step 4: Merge both types of edges (conceptual + contextual)
    combined_edges_df = aggregate_df(concept_edges_df, proximity_edges_df)

    # Step 5: Build the NetworkX graph from the edge list
    G = build_graph_from_df(combined_edges_df)

    # Step 6: Detect communities and assign colors for visualization
    communities = find_communities(G)
    G, _ = color_graph(G, communities)

    # Step 7: Save graph visualization JSON (e.g., for frontend use)
    week_str = datetime.datetime.now().strftime("%Y_%m_%d")
    output_dir = os.getenv("OUTPUT_DIR", "data/graphs")
    os.makedirs(output_dir, exist_ok=True)

    graph_viz_path = f"{output_dir}/graphs/knowledge_visualization/" 
    os.makedirs(graph_viz_path, exist_ok=True)

    write_graph_to_json(G, f"{graph_viz_path}/knowledge_graph.json")
    logger.info(f"Graph JSON saved to {graph_viz_path}/knowledge_graph.json")

    # Step 8: Save graph object as .gpickle for backend processing
    file_path = f"{output_dir}/graphs/kg_pickles/"  
    os.makedirs(file_path, exist_ok=True)

    with open(f"{file_path}/knowledge_graph_{week_str}.gpickle", 'wb') as f:
        pickle.dump(G, f, pickle.HIGHEST_PROTOCOL)

    logger.info(f"Graph object saved to {file_path}/knowledge_graph_{week_str}.gpickle")

    # Step 9: Save basic graph statistics for analysis and monitoring
    stats = compute_graph_metrics(G)
    
    logger.info("Knowledge graph construction completed successfully.")
    return G , stats


