import random
from typing import Dict, List
from .posting_interface import PostingInterface
from .post_manager import PostManager
from .llm_wrapper import ask_question
from .scoring import UserScoreTracker

class GameManager:
    def __init__(
        self,
        post_manager: PostManager,
        score_tracker: UserScoreTracker,
        posting_interface: PostingInterface,
        groups: Dict[str, str]
    ) -> None:
        self.post_manager = post_manager
        self.score_tracker = score_tracker
        self.posting_interface = posting_interface
        self.round = 1
        self.players = []
        self.groups = groups

    def add_player(self, username: str, player_group: str) -> None:
        """Add a player to the game if the username is unique.

        Args:
            username: The username of the player
            player_group: The group of the player

        Raises:
            ValueError: If the username is already taken
        """
        if any(player['username'] == username for player in self.players):
            raise ValueError(f"Username {username} is already taken.")
        self.players.append({'username': username, 'group': player_group})
        self.score_tracker.add_user(username)

    def get_least_represented_group(self) -> str:
        """Choose one of the least represented groups at random."""
        group_counts = {g: 0 for g in self.groups.keys()}
        for p in self.players:
            if p.get('group') in group_counts:
                group_counts[p['group']] += 1
        min_count = min(group_counts.values())
        least_represented_groups = [g for g, count in group_counts.items() if count == min_count]
        return random.choice(least_represented_groups)

    def get_player_group(self, username: str) -> str:
        """Return the group of the specified player."""
        for player in self.players:
            if player["username"] == username:
                return player["group"]
        return None

    def get_round(self) -> int:
        """Return the current round number."""
        return self.round

    def increment_round(self) -> None:
        """Advance the game to the next round and handle end-of-round logic."""
        self.score_tracker.initialize_round_scores(self.round + 1)
        posts = self.post_manager.get_posts_by_round(self.get_round())
        self.end_of_round_assessment(posts, self.get_round())
        self.score_tracker.centrality_points(posts, self.get_round())
        self.round += 1

    def end_of_round_assessment(self, posts: List[Dict], round: int) -> str:
        """Perform end-of-round group dominance assessment."""
        if posts is None:
            posts = self.posting_interface.get_posts_by_round(round)
        
        # Extract post content as a list
        posts_list = [post['message'] for post in posts]

        question = (
                "You are an expert in online community analysis and cultural trend recognition. "
                "Your task is to analyze the following social media posts to assess the collective vibe or emotional atmosphere they convey. "
                "Based on the overall tone, energy, and recurring themes, determine which of the listed groups best embodies the current mood. "
                "Consider factors such as optimism, sarcasm, intensity, playfulness, or seriousness. "
                "The goal is not to identify the most mentioned group, but to find the one whose identity, interests, and communication style "
                "most closely reflect the prevailing sentiment in the posts. "
                f"Posts: '{posts_list}' Groups: '{self.groups}'"
            )

        
        schema_dict = {
            "type": "object",
            "properties": {
                "assessment": {
                    "type": "object",
                    "properties": {
                        "dominant_group": {
                            "type": "string"
                        },
                        "tone_summary": {
                            "type": "string"
                        },
                        "alignment_reason": {
                            "type": "string"
                        }
                    },
                    "required": ["dominant_group"]
                }
            }
        }

        response = ask_question(question, schema_dict, 300)
        
        dominant_group = response["assessment"]["dominant_group"]
        for player in self.players:
            if player['group'] == dominant_group:
                self.score_tracker.dominant_network_slant(player['username'], round)
        return dominant_group

    def get_scores_for_round(self, round: int) -> Dict[str, int]:
        """Get user scores for a specific round."""
        scores = self.score_tracker.get_scores()
        round_scores = {user: scores[user].get(round, 0) for user in scores}
        return round_scores
