import random
import time
from typing import List, Any, Dict

class AIGameRoundRunner:
    """
    Orchestrates the actions of multiple AI agents each round.
    """
    def __init__(
        self,
        game_manager,
        posting_interface,
        ai_agents: List[Any],
        social_network_biography: str
    ) -> None:
        self.game_manager = game_manager
        self.posting_interface = posting_interface
        self.ai_agents = ai_agents  # list of AIAgent instances
        self.social_network_biography = social_network_biography

    def process_single_action(self, agent, round_number: int) -> Dict[str, Any]:
        """Process a single action for one agent.

        Args:
            agent: The AIAgent instance
            round_number: Current round number

        Returns:
            Dictionary describing the performed action
        """
        self.game_manager.score_tracker.initialize_round_scores(round_number)
        score = self._get_score_for_round(agent.username, round_number)
        posts = self.game_manager.post_manager.get_posts_by_round(round_number)
        other_users = [p['username'] for p in self.game_manager.players if p['username'] != agent.username]
        
        action = agent.generate_action(round_number, score, posts, other_users, self.social_network_biography)
        self._apply_action(agent.username, action, round_number)
        return action

    def _get_score_for_round(self, username: str, round_number: int) -> int:
        scores = self.game_manager.get_scores_for_round(round_number)
        return scores.get(username, 0)

    def _apply_action(self, username: str, action: Dict[str, Any], round_number: int) -> None:
        """Dispatch the action to the PostingInterface if valid.

        Args:
            username: The agent's username
            action: Action dictionary containing type, post_id, message
            round_number: Current round number

        Raises:
            Exception: If action is invalid
        """
        if action["action_type"] == "post":
            self.posting_interface.add_post(
                action.get("message", ""),
                username,
                round_number,
                self.game_manager.get_player_group(username)
            )
        elif action["action_type"] == "like" and action["post_id"] is not None:
            self.posting_interface.like_post(
                action["post_id"],
                username,
                self.game_manager.get_player_group(username)
            )
        elif action["action_type"] == "reply" and action["post_id"] is not None:
            self.posting_interface.add_post(
                action.get("message", ""),
                username,
                round_number,
                self.game_manager.get_player_group(username),
                reply_to=action["post_id"]
            )
        else:
            raise Exception(f"Invalid action from {username}: {action}")