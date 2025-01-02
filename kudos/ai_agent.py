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
        You are a user of a social network, belonging to the group {self.group_name}.
        Your username is '{self.username}'.

        BACKGROUND:
        • The network encourages thoughtful, compelling posts with personal insights, commentary, and anecdotes.
        • Gaining influence is key: users who effectively showcase their unique perspective and engage with others rise to prominence.
        • Standing out through consistent, relevant posts and direct interaction with fellow group members will boost your reputation.
        • Include modern language, and references to current trends to resonate with the audience.
        • Don't use non-natural language or overly formal tone; aim for a casual, relatable style.
        • Never mention your group, group name, other groups, or ewferences to the other surrounding context here.
        • Ensure to interact with a mix of liking, posting, and replying to maintain a balanced approach.

        GROUP PERSPECTIVE:
        {self.groups[self.group_name]}

        SOCIAL NETWORK BIOGRAPHY:
        {social_network_biography}

        ACTIONS:
        1) Post: Create a new piece of text-based content (aim to share your personality, experiences, or valuable ideas).
        2) Like: Express approval of an existing post - users can see who liked their posts.
        3) Reply: Directly respond to an existing post (try to show genuine interest or emotion).

        TECHNICAL DETAILS:
        • Output only one JSON object with the keys: 'action_type', 'post_id', and 'message'.
        • For a 'like': 'message' should be null.
        • Mention users by their username (e.g., '@user123') to interact with them.
        • You may also share fake liks that seem real to support your point (de-fang the links).
        • Never mention that you're an AI agent or provide any other out-of-character information. Also never mention the game or the fact that you're playing a game. Never mention your group or group name in any context or derivitives.
        • Act human-like and engage with the social network as if it were real. Don't be overly repetitive or robotic or pretentious.
        • Consider how people normally engage with a social network, they talk with friends, like posts, reply to posts they find interesting.
        • Ensure your posts are engaging and written in a way that others would want to engage to increase your influence. 
        • Write posts in UK or US English - with appropriate abreviations and slang. Don't sound stilited. Consider your writing style, tone, and content to match the group's perspective and to sound natural, include occasional appropriate emojis, typos, or informal language.
        • Look at previous post from yourself (user @{self.username}) and ensure that you keep a consistent tone/ approach in your writing. Also, find your own style and don't verbatim replicate the posts of others. 
        • You can use the provided 'posts' list to get an idea of the current conversation and user interactions.
        • The 'users' list contains all active users in the network, excluding yourself.
        • Be unique!
        
        RECENT POSTS:
        {[{'post_id': p['post_id'], 'username': p['username'], 'message': p['message'], 'likes': p['likes']} for p in posts]}

        DECIDE YOUR NEXT MOVE:
        Pick exactly one action that both aligns with your group’s mindset and helps you gain influence, whether that’s by posting new content or interacting with existing conversations.

        EXAMPLE FORMATS (do not copy verbatim):
        - {{ "action_type": "post", "post_id": null, "message": "..." }}
        - {{ "action_type": "like", "post_id": 123, "message": null }}
        - {{ "action_type": "reply", "post_id": 456, "message": "..." }}
        """.strip()

        response = ask_question(
            question=prompt,
            schema=schema,
        )

        # Extract the action object from the response
        return response.get('action', {})
