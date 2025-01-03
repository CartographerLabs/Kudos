from typing import Dict, List, Optional, Any
import random
import time
from collections import defaultdict

from .post_manager import PostManager
from .scoring import UserScoreTracker
from .posting_interface import PostingInterface
from .game_manager import GameManager
from .ai_agent import AIAgent
from .ai_game_round_runner import AIGameRoundRunner

class GameSimulator:
    """Provides a clean interface for running social network game simulations."""

    def __init__(
        self,
        network_groups: Dict[str, str],
        network_biography: str,
        game_rules: str,
        num_ai_players: int = 4,
        posts_file: str = 'simulation_posts.json',
        actions_per_user: int = 3
    ) -> None:
        """Initialize the game simulation environment.

        Args:
            network_groups: Mapping group name -> group description
            network_biography: Narrative describing the network
            game_rules: Overall rules for scoring and gameplay
            num_ai_players: Number of AI-controlled players
            posts_file: JSON file path for storing posts
            actions_per_user: Max actions per user in one round
        """
        self.post_manager = PostManager(posts_file)
        self.score_tracker = UserScoreTracker()
        self.game_manager = GameManager(
            self.post_manager,
            self.score_tracker,
            None,
            network_groups
        )
        self.posting_interface = PostingInterface(
            self.post_manager,
            network_biography,
            self.game_manager,
            self.score_tracker
        )
        self.game_manager.posting_interface = self.posting_interface
        
        # Setup AI players
        self.ai_agents = self._initialize_ai_agents(num_ai_players, game_rules)
        self.round_runner = AIGameRoundRunner(
            self.game_manager,
            self.posting_interface,
            self.ai_agents,
            network_biography
        )
        self.actions_per_user = actions_per_user

    def _generate_unique_username(self, base_names: List[str], existing_names: List[str]) -> str:
        """
        Generate a semi-random, unique username based on a list of base words.

        Args:
            base_names: List of base words to construct names from.
            existing_names: List of usernames that already exist.

        Returns:
            A unique username string.
        """
        def random_suffix(length=3):
            return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

        # Attempt to generate a unique name
        for _ in range(100):  # Limit to 100 attempts to avoid infinite loop
            base = random.choice(base_names)
            candidate_name = f"{base}_{random_suffix()}"
            if candidate_name not in existing_names:
                return candidate_name

        # Fallback if no unique name is found
        raise ValueError("Could not generate a unique username after 100 attempts.")

    def _initialize_ai_agents(self, num_agents: int, game_rules: str) -> List[AIAgent]:
        base_names = ["Alpha", "Beta", "Gamma", "Delta", "Echo"]  # Example base names
        existing_names = [agent.username for agent in self.ai_agents]

        agents = []
        for _ in range(num_agents):
            username = self._generate_unique_username(base_names, existing_names)
            existing_names.append(username)  # Ensure the generated name is tracked

            group = self.game_manager.get_least_represented_group()
            self.game_manager.add_player(username, group)
            agents.append(AIAgent(username, group, game_rules, self.game_manager.groups))

        return agents


    def run_simulation(
        self,
        num_rounds: int = 4,
        min_delay: float = 0.5,
        max_delay: float = 2.0,
        pause_between_rounds: bool = True
    ) -> Dict[str, Any]:
        """Run the complete game simulation.

        Args:
            num_rounds: Number of rounds to simulate
            min_delay: Minimum delay between actions (seconds)
            max_delay: Maximum delay between actions (seconds)
            pause_between_rounds: Prompt user before proceeding

        Returns:
            Dictionary containing final scores and other stats
        """
        for current_round in range(num_rounds):
            print(f"\n=== Starting Round {current_round + 1} ===")
            self._run_round(min_delay, max_delay)
            
            if pause_between_rounds:
                input("\nPress Enter to end round and see scores...")
            
            self.game_manager.increment_round()
            scores = self.game_manager.get_scores_for_round(self.game_manager.get_round() - 1)
            print(f"\nScores after Round {current_round + 1}:", scores)

        return self._get_final_results()

    def _run_round(self, min_delay: float, max_delay: float) -> None:
        """Execute a single round of the game.

        Args:
            min_delay: Minimum time to wait between actions
            max_delay: Maximum time to wait between actions
        """
        actions_remaining = defaultdict(lambda: self.actions_per_user)
        available_agents = self.ai_agents.copy()
        
        while available_agents:
            time.sleep(random.uniform(min_delay, max_delay))
            agent = random.choice(available_agents)
            
            action = self.round_runner.process_single_action(
                agent, 
                self.game_manager.get_round()
            )
            print(f"{agent.username} performed: {action['action_type']}")
            
            actions_remaining[agent.username] -= 1
            if actions_remaining[agent.username] == 0:
                available_agents.remove(agent)

    def _get_final_results(self) -> Dict[str, Any]:
        """Compile final simulation results.

        Returns:
            Dictionary of final scores, total posts, and agent groups
        """
        return {
            'final_scores': self.score_tracker.get_scores(),
            'total_posts': len(self.post_manager._read_posts_from_json()),
            'groups': {agent.username: agent.group_name for agent in self.ai_agents}
        }

    def get_state(self) -> Dict[str, Any]:
        """Get current simulation state.

        Returns:
            Dictionary with current round, scores, and players
        """
        return {
            'current_round': self.game_manager.get_round(),
            'scores': self.score_tracker.get_scores(),
            'players': self.game_manager.players
        }
