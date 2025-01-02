from typing import Dict, List, Any
import networkx as nx
import re

def get_mentions(post: Dict[str, Any]) -> List[str]:
    """Extract mentioned usernames from post content.

    Args:
        post: Post dictionary containing message content

    Returns:
        List of usernames mentioned in the post
    """
    return re.findall(r'@(\w+)', post['message'])

def create_graph_and_get_centrality(posts: List[Dict[str, Any]]) -> Dict[str, float]:
    """Calculate user influence based on interaction network.

    Args:
        posts: List of post dictionaries

    Returns:
        Dictionary mapping usernames to centrality scores
    """
    G = nx.DiGraph()
    for post in posts:
        G.add_node(post['username'])
        if post['reply_to']:
            replied_post = next((p for p in posts if p['post_id'] == post['reply_to']), None)
            if replied_post:
                G.add_edge(post['username'], replied_post['username'])
        mentions = get_mentions(post)
        for mention in mentions:
            G.add_edge(post['username'], mention)
    return nx.degree_centrality(G)