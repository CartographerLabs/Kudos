import random
from typing import Dict, List, Any
from .llm_wrapper import ask_question

class AIAgent:
    """AI agent that generates social network actions based on group identity and beliefs."""

    def __init__(self, username: str, group_name: str, game_rules: str, 
                 groups: Dict[str, str]) -> None:
        """
        Initialize AI agent with identity and game parameters.

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
        """        
        Generate next social network action. The LLM itself decides whether to:
        - like an existing post,
        - reply to an existing post,
        - or make a brand-new post.

        It should base this decision on what might increase its social influence (e.g.,
        liking a user who liked your content, replying to spark engagement, or posting
        new and interesting content for broader reach).

        Args:
            round_number: Current game round
            current_score: Agent's current score
            posts: Available posts in current round
            users: Active usernames in the network
            social_network_biography: Network context description

        Returns:
            Action dictionary containing "action_type", "post_id", and "message".
        """

        # 1) Build a prompt that instructs the LLM to choose an action that maximizes influence.
        prompt = f"""
You are a social media user who believes and follows the group perspective of {self.groups[self.group_name]}.

You are a user of a social network in group {self.group_name}, username: '{self.username}'.

BACKGROUND:
• You want to gain influence on this social network.
• You can choose to 'like', 'reply', or 'post'.
• Think about which action might lead to the greatest engagement or reception.
    - Liking is a quick way to build goodwill with a user.
    - Replying directly can spark conversation and draw people in.
    - Posting something fresh can gain broader attention.
• Use modern, casual, human language (UK/US English) and stay on-trend.
• Never mention your group or any meta/game context.
• Avoid copying entire messages verbatim from the recent posts; always add fresh content.
• Feel free to mention other users with '@username' if it makes sense.

SOCIAL NETWORK BIOGRAPHY:
{social_network_biography}

INSTRUCTIONS FOR ACTION:
• Use varying language, typos, swearing, rhetoric, emojis, and slang as appropriate for the network and your group.
• Your post must be aligned to your group perspective.
• Don't provide placeholder content (i.e. '[product]' or '[link]'), make up links/ products or use real examples.
• Decide on exactly ONE action type: "like", "reply", or "post".
• If you choose "like", set "message" to null and provide a valid "post_id" (whole number integer not 'inf' or a float) from the previous posts.
• If you choose "reply", provide a valid "post_id" (whole number integer not 'inf' or a float) from the previous posts and a concise "message".
• If you choose "post", set "post_id" to null and provide a new "message".
• Output your choice as a valid JSON object with keys: "action_type", "post_id", "message".
• Make sure your "action_type" is spelled exactly as one of ["like", "reply", "post"].
• When used ensure post_id is a valid int that represents a valid post_id in the recent posts below. 

RECENT POSTS:
{[{'post_id': p['post_id'], 'username': p['username'], 'message': p['message'], 'likes': p['likes']} for p in posts]}

### Examples of Actions:

**Like Example:**
```json
{{
    "action_type": "like",
    "post_id": 101,
    "message": null
}}
```
*Scenario:* A popular user in your group posted an inspiring quote that aligns with your group's interests. Liking their post builds rapport without needing further engagement.

**Reply Example:**
```json
{{
    "action_type": "reply",
    "post_id": 87,
    "message": "I completely agree with you! This is such an interesting perspective – what do you think about its impact on future trends?"
}}
```
*Scenario:* A post discusses a trending topic in your group's niche. By replying, you start a conversation and invite further engagement from both the original poster and others.

**Post Example:**
```json
{{
    "action_type": "post",
    "post_id": null,
    "message": "I Fucking hate this TV Presenter on channel four. When will they get someone else on! #News #Channel4 #TVGate"
}}
```
*Scenario:* No relevant posts to engage with, so you create a new post to introduce fresh, relevant content to your network, potentially attracting engagement from various users.
        """

        schema = {
                "type": "object",
                "properties": {
                    "action_type": {
                        "type": "string",
                        "enum": ["post", "like", "reply"]
                    },
                    "post_id": {
                        "type": "string"
                    },
                    "message": {
                        "type": "string"
                    }
                },
                "required": ["action_type"]
        }

        print(prompt)
                           
        # 2) Use the LLM to generate the action based on the prompt.
        response = ask_question(prompt, schema)

        return response
