import random
from typing import Dict, List, Any
from .llm_wrapper import ask_question

class AIAgent:
    """AI agent that generates social network actions based on group identity and beliefs."""

    def __init__(self, username: str, group_name: str, game_rules: str, 
                 groups: Dict[str, str]) -> None:
        """Initialize AI agent with identity and game parameters.

        Args:
            username: Agent's unique identifier
            group_name: Agent's assigned social group
            game_rules: Ruleset governing agent behavior
            groups: Mapping of group names to their characteristics
        """
        self.username = username
        self.group_name = group_name
        self.game_rules = game_rules
        self.groups = groups

    def generate_action(self, round_number: int, current_score: int,
                       posts: List[Dict[str, Any]], users: List[str], 
                       social_network_biography: str) -> Dict[str, Any]:
        """Generate next social network action based on current state.

        Args:
            round_number: Current game round
            current_score: Agent's current score
            posts: Available posts in current round
            users: Active usernames in the network
            social_network_biography: Network context description

        Returns:
            Action dictionary containing "action_type", "post_id", and "message".
        """

        # 1) Randomly choose the action instead of letting the LLM decide.
        chosen_action_type = random.choice(["like", "post", "reply"])

        # 2) Build a sub-prompt that depends on the chosen_action_type.
        if chosen_action_type == "like":
            sub_prompt = (
                "You must perform a 'like' action. "
                "Choose exactly one post to like. "
                "Set 'message' to null, and provide the 'post_id'."
            )
        elif chosen_action_type == "reply":
            sub_prompt = (
                "You must perform a 'reply' action. "
                "Choose exactly one post to reply to. "
                "Provide the 'post_id' and craft a short 'message' with fresh content."
            )
        else:  # chosen_action_type == "post"
            sub_prompt = (
                "You must perform a 'post' action. "
                "Create a new message in 'message' and set 'post_id' to null."
            )

        # 3) Updated prompt that explicitly states the action is already chosen
        prompt = f"""
You are a user of a social network in group {self.group_name}, username: '{self.username}'.

BACKGROUND:
• Share unique, personal insights to gain influence.
• Use modern language, casual style, and stay current with trends.
• Never mention your group or any outside context.
• Engage by liking, posting, or replying in balanced ways.
• Avoid repeating or copying entire messages from previous posts; always contribute fresh content.

GROUP PERSPECTIVE:
{self.groups[self.group_name]}

SOCIAL NETWORK BIOGRAPHY:
{social_network_biography}

YOUR ASSIGNED ACTION: {chosen_action_type.upper()}
{sub_prompt}

TECHNICAL DETAILS:
• Output one JSON object: "action_type", "post_id", and "message".
• For a "like", "message" must be null.
• Mention other users with "@username" if relevant.
• Maintain a human-like tone; never mention AI or the game context.
• Keep your style consistent, and do not replicate or paraphrase full previous posts.
• Write in natural UK/US English.

RECENT POSTS:
{[{'post_id': p['post_id'], 'username': p['username'], 'message': p['message'], 'likes': p['likes']} for p in posts]}
"""

        # Schema remains the same, but we expect the LLM to fill out details
        # for the chosen_action_type rather than deciding it.
        schema = {
            "type": "object",
            "properties": {
                "action": {
                    "type": "object",
                    "properties": {
                        "action_type": {
                            "type": "string",
                            "enum": ["post", "like", "reply"]
                        },
                        "post_id": {
                            "type": "number"
                        },
                        "message": {
                            "type": "string"
                        }
                    },
                    "required": ["action_type"]
                }
            }
        }

        # 4) Ask the LLM for the action details (post_id, message)
        response = ask_question(
            question=prompt,
            schema=schema,
        )

        # 5) Parse the LLM response but enforce our chosen_action_type
        action = response.get('action', {})
        action['action_type'] = chosen_action_type  # Ensure it matches our choice

        # Return the final action object
        return action
