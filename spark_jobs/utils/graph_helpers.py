import uuid
import random
import json
from tqdm import tqdm
import re
import pandas as pd
import numpy as np
import seaborn as sns
import networkx as nx
from networkx.readwrite import json_graph
from networkx.algorithms.community import girvan_newman
from utils.prompts import generate_completion , graphPrompt
from langchain_community.document_loaders.dataframe import DataFrameLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

tqdm.pandas(desc="Processing DataFrame")

def split_text_into_chunks(df: pd.DataFrame, chunk_size: int = 1000) -> list:
    """
    Splits a long text into smaller chunks of specified size.
    
    Args:
        df (pd.DataFrame): The DataFrame containing the text to be split.
        chunk_size (int): The maximum size of each chunk.
    """
    loader = DataFrameLoader(df, page_content_column="content", engine = "pandas")
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size)
    return text_splitter.split_documents(documents)




def documents2DataFrame(documents) -> pd.DataFrame:
    rows = []
    for chunk in documents:
        row = {
            "text": chunk.page_content,
            **chunk.metadata,
            "chunk_id": uuid.uuid4().hex,
        }
        rows = rows + [row]

    df = pd.DataFrame(rows)
    return df



def df2Graph(dataframe: pd.DataFrame) -> list:
    # dataframe.reset_index(inplace=True)
    results = dataframe.progress_apply(
        lambda row: graphPrompt(row.text, {"chunk_id": row.chunk_id}), axis=1
    )
    # invalid json results in NaN
    results = results.dropna()
    results = results.reset_index(drop=True)

    ## Flatten the list of lists to one single list of entities.
    concept_list = np.concatenate(results).ravel().tolist()
    return concept_list


def graph2Df(nodes_list) -> pd.DataFrame:
    ## Remove all NaN entities
    graph_dataframe = pd.DataFrame(nodes_list).replace(" ", np.nan)
    graph_dataframe = graph_dataframe.dropna(subset=["node_1", "node_2"])
    graph_dataframe["node_1"] = graph_dataframe["node_1"].apply(lambda x: x.lower())
    graph_dataframe["node_2"] = graph_dataframe["node_2"].apply(lambda x: x.lower())

    return graph_dataframe

def post_process_concepts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Post-process a DataFrame containing graph data.
    
    Args:
        df (pd.DataFrame): A DataFrame containing the graph data.

    Returns:
        pd.DataFrame: A DataFrame with the processed graph data.
    """
    df.replace("", np.nan, inplace=True)
    df.dropna(subset=["node_1", "node_2", 'edge'], inplace=True)
    df['count'] = 4 # Assuming a default count of 4 for each edge
    return df

def contextual_proximity(df: pd.DataFrame) -> pd.DataFrame:
    ## Melt the dataframe into a list of nodes
    dfg_long = pd.melt(
        df, id_vars=["chunk_id"], value_vars=["node_1", "node_2"], value_name="node"
    )
    dfg_long.drop(columns=["variable"], inplace=True)
    # Self join with chunk id as the key will create a link between terms occuring in the same text chunk.
    dfg_wide = pd.merge(dfg_long, dfg_long, on="chunk_id", suffixes=("_1", "_2"))
    # drop self loops
    self_loops_drop = dfg_wide[dfg_wide["node_1"] == dfg_wide["node_2"]].index
    dfg2 = dfg_wide.drop(index=self_loops_drop).reset_index(drop=True)
    ## Group and count edges.
    dfg2 = (
        dfg2.groupby(["node_1", "node_2"])
        .agg({"chunk_id": [",".join, "count"]})
        .reset_index()
    )
    dfg2.columns = ["node_1", "node_2", "chunk_id", "count"]
    dfg2.replace("", np.nan, inplace=True)
    dfg2.dropna(subset=["node_1", "node_2"], inplace=True)
    # Drop edges with 1 count
    dfg2 = dfg2[dfg2["count"] != 1]
    dfg2["edge"] = "contextual proximity"
    return dfg2

def aggregate_df(dfg1: pd.DataFrame, dfg2: pd.DataFrame) -> pd.DataFrame:
    dfg = pd.concat([dfg1, dfg2], axis=0)
    dfg = (
        dfg.groupby(["node_1", "node_2"])
        .agg({"chunk_id": ",".join, "edge": ','.join, 'count': 'sum'})
        .reset_index()
    )
    return dfg

def build_graph_from_df(df: pd.DataFrame) -> nx.Graph:
    """
    Build a graph from a DataFrame containing nodes and edges.
    
    Args:
        df (pd.DataFrame): A DataFrame containing the graph data.

    Returns:
        nx.Graph: A NetworkX graph object.
    """

    nodes = pd.concat([df['node_1'], df['node_2']], axis=0).unique()
    G = nx.Graph()

    ## Add nodes to the graph
    for node in nodes:
        G.add_node(
            str(node)
        )

    ## Add edges to the graph
    for index, row in df.iterrows():
        G.add_edge(
            str(row["node_1"]),
            str(row["node_2"]),
            title=row["edge"],
            weight=row['count']/4
        )
    return G

def find_communities(G: nx.Graph) -> list:
    communities_generator = nx.community.girvan_newman(G)
    #top_level_communities = next(communities_generator)
    next_level_communities = next(communities_generator)
    communities = sorted(map(sorted, next_level_communities))
    return communities

def color_graph(G: nx.Graph, communities: list) -> tuple:
    palette = "hls"

    ## Define a color palette
    p = sns.color_palette(palette, len(communities)).as_hex()
    random.shuffle(p)
    rows = []
    group = 0
    for community in communities:
        color = p.pop()
        group += 1
        for node in community:
            rows += [{"node": node, "color": color, "group": group}]

    df_colors = pd.DataFrame(rows)

    #Add colors to the graph nodes
    for index, row in df_colors.iterrows():
        G.nodes[row['node']]['group'] = row['group']
        G.nodes[row['node']]['color'] = row['color']
        G.nodes[row['node']]['size'] = G.degree[row['node']]

    return G, df_colors

def write_graph_to_json(G: nx.Graph, path: str) -> None:
    """
    Write a NetworkX graph to a JSON file.
    
    Args:
        G (nx.Graph): A NetworkX graph object.
        path (str): The file path where the graph will be saved.
    """
    data = json_graph.node_link_data(G)
    with open(path, 'w') as f:
        json.dump(data, f)

def get_top_n(centrality_dict, n=5):
    return sorted(centrality_dict.items(), key=lambda x: x[1], reverse=True)[:n]
    
def get_top_node_names(centrality_dict, n=5):
    return sorted(centrality_dict.items(), key=lambda x: x[0], reverse=True)[:n]

def compute_graph_metrics(G: nx.Graph, top_n: int = 5) -> dict:
    """
    Compute global and node-level metrics for a NetworkX graph.

    Args:
        G (nx.Graph): A NetworkX graph object.
        top_n (int): Number of top nodes to return for each centrality metric.

    Returns:
        dict: A dictionary containing graph-level stats and top node metrics.
    """
    # Community detection (first-level Girvan-Newman split)
    try:
        first_level = next(girvan_newman(G))
        communities = list(first_level)
    except Exception:
        communities = []

    # Average path length, only if graph is connected
    try:
        avg_path_length = nx.average_shortest_path_length(G)
    except:
        avg_path_length = None

    # Node-level centralities
    degree_centrality = nx.degree_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)
    page_rank = nx.pagerank(G)

    # Compile metrics
    metrics = {
        "global": {
            "nodes": G.number_of_nodes(),
            "edges": G.number_of_edges(),
            "density": nx.density(G),
            "communities": len(communities),
            "global_clustering_coefficient": nx.transitivity(G),
            "average_path_length": avg_path_length
        },
        "top_nodes": {
            "nodes": get_top_node_names(degree_centrality, top_n),
            "degree_centrality": get_top_n(degree_centrality, top_n),
            "betweenness_centrality": get_top_n(betweenness_centrality, top_n),
            "closeness_centrality": get_top_n(closeness_centrality, top_n),
            "page_rank": get_top_n(page_rank, top_n)
        }
    }

    return metrics


# API for generating completion using a language model
def batch_generate_completion(texts, system_prompt):
    user_prompt = "Classify these news articles:\n" + "\n".join(
        f"{i+1}. {text.strip()}" for i, text in enumerate(texts)
    )

    chat_response = generate_completion(
        system_prompt=system_prompt,
        user_prompt=user_prompt
    )

    output = chat_response.strip()
    lines = output.splitlines()

    # Clean & validate
    categories = []
    for line in lines:
        match = re.match(r"^\d+\.\s*(.+)", line)
        if match:
            categories.append(match.group(1).strip())
    return categories

def classify_in_batches(df, system_prompt, batch_size=10):
    results = []
    for i in tqdm(range(0, len(df), batch_size)):
        batch = df.iloc[i:i+batch_size]
        texts = batch["description"].tolist()
        categories = batch_generate_completion(texts, system_prompt=system_prompt)
        results.extend(categories)

    return results
