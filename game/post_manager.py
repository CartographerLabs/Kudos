from typing import List, Dict, Optional, Any
import json
import os
from datetime import datetime
from filelock import FileLock

class PostManager:
    """Manages social network posts with thread-safe file operations."""

    def __init__(self, file_path: str) -> None:
        """Initialize PostManager with a file path.

        Args:
            file_path: Path to JSON file storing posts
        """
        self.file_path = file_path
        self.game_manager: Optional[Any] = None

    def _read_posts_from_json(self) -> List[Dict[str, Any]]:
        """Read posts from JSON file with thread-safety.

        Returns:
            List of post dictionaries
        """
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, 'r') as file:
            return json.load(file)

    def _write_posts_to_json(self, posts: List[Dict[str, Any]]) -> None:
        """Write posts to JSON file with thread-safety.

        Args:
            posts: List of post dictionaries to write
        """
        with open(self.file_path, 'w') as file:
            json.dump(posts, file, indent=4)

    def like_post(self, post_id: int, username: str) -> bool:
        """
        Like a post by its ID.

        Args:
            post_id (int): The ID of the post to like.
            username (str): The username of the person liking the post.

        Returns:
            bool: True if the post was liked, False otherwise.
        """
        lock = FileLock(f"{self.file_path}.lock")
        with lock:
            posts = self._read_posts_from_json()
            for post in posts:
                if post['post_id'] == post_id:
                    if username not in post['likes']:
                        post['likes'].append(username)
                        self._write_posts_to_json(posts)
                        return True
            return False

    def add_post(self, message: str, username: str, round: Any, poster_group: str, likes: Optional[List[str]] = None, reply_to: Optional[int] = None, is_removed: bool = False) -> None:
        """
        Add a new post to the JSON file.

        Args:
            message (str): The message of the post.
            username (str): The username of the poster.
            poster_group (str): The group of the poster.
            likes (list, optional): A list of usernames who like the post. Defaults to an empty list.
            reply_to (int, optional): The ID of the post being replied to. Defaults to None.
            round: The round of the post. Defaults to None.
        """
        lock = FileLock(f"{self.file_path}.lock")
        with lock:
            if is_removed:
                message = "This post has been removed."

            if likes is None:
                likes = []
            posts = self._read_posts_from_json()
            post_id = max([post['post_id'] for post in posts], default=0) + 1
            new_post = {
                'message': message,
                'username': username,
                'poster_group': poster_group,
                'likes': likes,
                'reply_to': reply_to,
                'post_id': post_id,
                'is_removed': is_removed,
                'round': round,
                'timestamp': datetime.now().isoformat()
            }
            posts.append(new_post)
            self._write_posts_to_json(posts)

    def get_posts_by_round(self, round: Any) -> List[Dict[str, Any]]:
        """
        Get all posts for a given round.

        Args:
            round: The round to filter posts by.

        Returns:
            list: A list of posts for the given round.
        """
        lock = FileLock(f"{self.file_path}.lock")
        with lock:
            posts = self._read_posts_from_json()
            return [post for post in posts if post['round'] == round]

    def get_post_by_id(self, post_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a post by its ID.

        Args:
            post_id (int): The ID of the post to retrieve.

        Returns:
            dict: The post with the given ID, or None if not found.
        """
        lock = FileLock(f"{self.file_path}.lock")
        with lock:
            posts = self._read_posts_from_json()
            for post in posts:
                if post['post_id'] == post_id:
                    return post
            return None

