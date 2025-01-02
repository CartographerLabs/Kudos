import networkx as nx
from .misc import create_graph_and_get_centrality
from typing import List, Dict, Any

class UserScoreTracker:
    def __init__(self) -> None:
        self.scores = {}

    def add_user(self, user_id: str) -> None:
        """Initialize user scores with 0 for current round."""
        if user_id not in self.scores:
            self.scores[user_id] = {}

    def add_points(self, user_id: str, points: int, round: int) -> None:
        if round not in self.scores[user_id]:
            self.scores[user_id][round] = 0
        self.scores[user_id][round] += points

    def subtract_points(self, user_id: str, points: int, round: int) -> None:
        if round not in self.scores[user_id]:
            self.scores[user_id][round] = 0
        self.scores[user_id][round] -= points

    def like_on_post(self, username: str, round: int) -> None:
        self.add_points(username, 1, round)

    def reply_on_post(self, username: str, round: int) -> None:
        self.add_points(username, 1, round)

    def like_group_mate_post(self, username: str, round: int) -> None:
       self.add_points(username, 1, round)

    def dominant_network_slant(self, username: str, round: int) -> None:
        self.add_points(username, 3, round)

    def centrality_points(self, posts: List[Dict[str, Any]], round: int) -> None:
        """Add points for top 5% of users by centrality."""
        centrality = create_graph_and_get_centrality(posts)
        top_5_percent = sorted(centrality, key=centrality.get, reverse=True)[:max(1, len(centrality) // 20)]
        for user in top_5_percent:
            self.add_user(user)
            self.add_points(user, 2, round)

    def misalignment_penalty(self, username: str, round: int) -> None:
        self.subtract_points(username, 1, round)

    def get_scores(self) -> Dict[str, Dict[int, int]]:
        """Get the current scores of all users."""
        return self.scores

    def initialize_round_scores(self, round: int) -> None:
        for user_id in self.scores:
            if round not in self.scores[user_id]:
                self.scores[user_id][round] = 0