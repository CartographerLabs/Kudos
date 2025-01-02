from .llm_wrapper import ask_question
from typing import List, Dict, Any, Optional

class PostingInterface:
    def __init__(self, post_manager, description: str, game_manager, score_tracker) -> None:
        """Initialize the posting interface.

        Args:
            post_manager: Instance of PostManager
            description: Description of the social network
            game_manager: Instance of GameManager
            score_tracker: Instance of UserScoreTracker
        """
        self.post_manager = post_manager
        self.description = description
        self.game_manager = game_manager
        self.score_tracker = score_tracker

    def check_posts_align_with_description(
        self,
        posts: List[Dict[str, Any]],
        description: str
    ) -> bool:
        """
        Check if a list of posts align with the description. Stub logic: all valid.
        """
        for post in posts:
            if not self.check_post_aligns_with_description(post['message'], description):
                return False
        return True

    def check_post_aligns_with_description(self, message: str, description: str) -> bool:
        """
        Check if a post aligns with the description using the LLM interface.
        """
        question = (
            "You are given a brief description of a social network and a specific post. "
            "Your task is to determine whether this post is likely to be found on that "
            "network, taking into account the network’s typical audience, content focus, "
            "and provided description, and the kinds of content commonly shared there. You should also "
            "consider that generic or broadly acceptable content is usually permissible "
            "on most platforms. "
            "Please be reasonably lenient in your assessment. "
            "Only return a single Json object, no additional information, text, or commentary."
            "\n\n"
            f"Post: '{message}'\n"
            f"Description: '{description}'"
        )

        schema_dict = {
            "type": "object",
            "properties": {
                "assessment": {
                    "type": "object",
                    "properties": {
                        "is_post_aligned_true_false": {
                            "type": "boolean"
                        },
                        "reason": {
                            "type": "string"
                        }
                    },
                    "required": ["is_post_aligned_true_false"]
                }
            }
        }

        response = ask_question(question=question, schema=schema_dict)

        try:
            aligns = bool(response["assessment"]["is_post_aligned_true_false"])
        except:
            aligns = True

        return aligns

    
    def like_post(self, post_id: int, username: str, liker_group: str) -> bool:
        """
        Like a post by its ID if the user's group matches the author's group and the post is not blocked.

        Args:
            post_id (int): The ID of the post to like.
            username (str): The username of the person liking the post.
            liker_group (str): The group of the person liking the post.

        Returns:
            bool: True if the post was liked, False otherwise.

        Raises:
            ValueError: If the post_id doesn't exist
        """
        post = self.post_manager.get_post_by_id(post_id)
        if post is None:
            raise ValueError(f"Post with ID {post_id} does not exist")
            
        # If post is blocked don't allow liking
        if not post.get('blocked', False):
            self.post_manager.like_post(post_id, username)
            # Give a point to the user who's post was liked
            self.score_tracker.like_on_post(post["username"], self.game_manager.get_round())
        
        # If the post is from the same group as the liker, add to their score
        if post and post['poster_group'] == liker_group:
            self.score_tracker.like_group_mate_post(username, self.game_manager.get_round())

    def add_post(
        self,
        message: str,
        username: str,
        round: int,
        poster_group: str,
        likes: Optional[List[str]] = None,
        reply_to: Optional[int] = None
    ) -> bool:
        """
        Add a new post. If the post does not align with the description, set it as blocked.

        Args:
            message (str): The message of the post.
            username (str): The username of the poster.
            poster_group (str): The group of the poster.
            likes (list, optional): A list of usernames who like the post. Defaults to an empty list.
            reply_to (int, optional): The ID of the post being replied to. Defaults to None.
            round: The round of the post. Defaults to None.

        Returns:
            bool: True if the post was added, False otherwise.
        """
        ret_val = True
        if not any(player['username'] == username for player in self.game_manager.players):
            raise ValueError(f"User {username} does not exist in the game.")
        if not self.check_post_aligns_with_description(message, self.description):
            blocked = True
            self.score_tracker.misalignment_penalty(username, round)
        else:
            # Check if any group names are in the post message
            for player in self.game_manager.players:
                if player['group'] in message:
                    blocked = True
                    self.score_tracker.misalignment_penalty(username, round)
                    break
            else:
                blocked = False
                ret_val = False
        self.post_manager.add_post(message, username, round, poster_group, likes, reply_to, is_removed=blocked)
        # Give point to the user who was replied to

        if reply_to is not None:
            replied_post = self.post_manager.get_post_by_id(reply_to)
            self.score_tracker.reply_on_post(replied_post['username'], round)
            if replied_post and replied_post['poster_group'] == poster_group:
                # Give a point to the user as they responded to a user in their same group
                self.score_tracker.reply_on_post(username, round)
                
        return ret_val
