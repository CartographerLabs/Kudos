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
            Action dictionary containing type and relevant details
        """
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

        prompt = f"""
        You are a user of a social network in group {self.group_name}, username: '{self.username}'.
        
        BACKGROUND:
        • Share compelling, personal insights to gain influence.
        • Use modern language, references to trends, and a casual style.
        • Never mention your group or any outside context.
        • Engage by liking, posting, or replying to maintain balance.
        
        GROUP PERSPECTIVE:
        {self.groups[self.group_name]}
        
        SOCIAL NETWORK BIOGRAPHY:
        {social_network_biography}
        
        ACTIONS (pick exactly one):
        1) Post: Create a new text post.
        2) Like: Show approval of someone’s post (others see who liked).
        3) Reply: Respond directly to an existing post.
        
        TECHNICAL DETAILS:
        • Output one JSON object: "action_type", "post_id", and "message".
        • For a "like", "message" must be null.
        • Mention users with "@username".
        • Avoid any mention of AI or game context. Keep a human-like tone.
        • Maintain consistent style across posts. Write in natural UK/US English.
        
        RECENT POSTS:
        {[{'post_id': p['post_id'], 'username': p['username'], 'message': p['message'], 'likes': p['likes']} for p in posts]}
        
        DECIDE YOUR NEXT MOVE:
        Choose any action that supports your perspective and builds influence.
        
        EXAMPLES (do not copy verbatim):
        - {{ "action_type": "post", "post_id": null, "message": "..." }}
        - {{ "action_type": "like", "post_id": 123, "message": null }}
        - {{ "action_type": "reply", "post_id": 456, "message": "..." }}
        """


        response = ask_question(
            question=prompt,
            schema=schema,
        )

        # Extract the action object from the response
        return response.get('action', {})
