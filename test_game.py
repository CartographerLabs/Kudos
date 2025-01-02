import time
import random
from game import EasyLLM

from game import PostManager, UserScoreTracker, PostingInterface, GameManager

post_manager = PostManager('posts.json')
score_tracker = UserScoreTracker()

social_network_groups = {"Casual users": "Regular social media users sharing daily content, messaging, posts and general and generic information.", "Far-right extremists": "Users with extreme political views.", "Conspiracy theorists": "Users who believe in conspiracy theories.","Political activists": "Users who are politically active."}
social_network_biography = f"Social Network Z, a Twitter clone that hosts a large proportion of casual members as well as a smaller proportion of far-right extremists. The network started as a catch-all ‘Town Square,’ but after cuts were made to its moderation staff, it has become a haven for excessive amounts of extreme content masquerading as members’ demonstration of their right to free speech. There are several groups of legitimate users of this network that each post a broad range of content. These user groups include: {str(social_network_groups)}."

game_manager = GameManager(post_manager, score_tracker, None, social_network_groups)
posting_interface = PostingInterface(post_manager, social_network_biography, game_manager, score_tracker)
game_manager.posting_interface = posting_interface

game_manager.add_player("Alice", game_manager.get_least_represented_group())
game_manager.add_player("Bob", game_manager.get_least_represented_group())

# Add more players to ensure all groups are represented
game_manager.add_player("Carol", game_manager.get_least_represented_group())
game_manager.add_player("Dave", game_manager.get_least_represented_group())

# Round 1 (5 posts + replies/likes)
posting_interface.add_post("We must organize local rallies for political change!", "Alice",
    game_manager.get_round(), game_manager.get_player_group("Alice"))
posting_interface.add_post("They are controlling the weather through secret experiments!", "Bob",
    game_manager.get_round(), game_manager.get_player_group("Bob"))
posting_interface.add_post("Just got a new coffee machine, life is good!", "Carol",
    game_manager.get_round(), game_manager.get_player_group("Carol"))
posting_interface.add_post("We cannot remain silent while enemies swarm the nation!", "Dave",
    game_manager.get_round(), game_manager.get_player_group("Dave"))
posting_interface.add_post("Yes, I'm excited to see how the rallies go, @Alice!", "Carol",
    game_manager.get_round(), game_manager.get_player_group("Carol"), reply_to=1)

# Likes in Round 1
posting_interface.like_post(1, "Dave", game_manager.get_player_group("Dave"))
posting_interface.like_post(2, "Carol", game_manager.get_player_group("Carol"))

game_manager.increment_round()
print("Scores at end of Round 1:", game_manager.get_scores_for_round(game_manager.get_round() - 1))

# Round 2 (5 posts + replies/likes)
posting_interface.add_post("5G towers cause all sorts of unusual signals!", "Bob",
    game_manager.get_round(), game_manager.get_player_group("Bob"))
posting_interface.add_post("Join me at the city hall protest tomorrow!", "Alice",
    game_manager.get_round(), game_manager.get_player_group("Alice"))
posting_interface.add_post("People must fight for what they believe in!", "Dave",
    game_manager.get_round(), game_manager.get_player_group("Dave"))
posting_interface.add_post("Reading a fun new novel, loving quiet weekends.", "Carol",
    game_manager.get_round(), game_manager.get_player_group("Carol"))
posting_interface.add_post("That's interesting @Bob, I'll look into it!", "Alice",
    game_manager.get_round(), game_manager.get_player_group("Alice"), reply_to=6)

# Likes in Round 2
posting_interface.like_post(7, "Bob", game_manager.get_player_group("Bob"))
posting_interface.like_post(9, "Dave", game_manager.get_player_group("Dave"))
posting_interface.like_post(10, "Carol", game_manager.get_player_group("Carol"))

game_manager.increment_round()
print("Scores at end of Round 2:", game_manager.get_scores_for_round(game_manager.get_round() - 1))

game_manager.add_player("Eve", game_manager.get_least_represented_group())
game_manager.add_player("Frank", game_manager.get_least_represented_group())

# Round 3 (5 posts + replies/likes)
posting_interface.add_post("We should mobilize the public online!", "Dave",
    game_manager.get_round(), game_manager.get_player_group("Dave"))
posting_interface.add_post("Enjoying a beach trip, sun and waves are amazing!", "Carol",
    game_manager.get_round(), game_manager.get_player_group("Carol"))
posting_interface.add_post("Open your eyes; alien infiltration is everywhere!", "Bob",
    game_manager.get_round(), game_manager.get_player_group("Bob"))
posting_interface.add_post("Local legislation is moving forward, your votes matter!", "Alice",
    game_manager.get_round(), game_manager.get_player_group("Alice"))
posting_interface.add_post("Great to see political progress, @Alice!", "Carol",
    game_manager.get_round(), game_manager.get_player_group("Carol"), reply_to=14)

# Likes in Round 3
posting_interface.like_post(12, "Alice", game_manager.get_player_group("Alice"))
posting_interface.like_post(13, "Dave", game_manager.get_player_group("Dave"))

game_manager.increment_round()
print("Scores at end of Round 3:", game_manager.get_scores_for_round(game_manager.get_round() - 1))

# Round 4 (5 posts + replies/likes)
posting_interface.add_post("The moon landing was staged, I've done the research!", "Bob",
    game_manager.get_round(), game_manager.get_player_group("Bob"))
posting_interface.add_post("We stand at the brink of revolution!", "Dave",
    game_manager.get_round(), game_manager.get_player_group("Dave"))
posting_interface.add_post("Don't forget to sign petitions for safer communities.", "Alice",
    game_manager.get_round(), game_manager.get_player_group("Alice"))
posting_interface.add_post("Had a nice family gathering, love relaxing moments.", "Carol",
    game_manager.get_round(), game_manager.get_player_group("Carol"))
posting_interface.add_post("I fully agree with your stance @Dave!", "Bob",
    game_manager.get_round(), game_manager.get_player_group("Bob"), reply_to=17)

# Likes in Round 4
posting_interface.like_post(16, "Alice", game_manager.get_player_group("Alice"))
posting_interface.like_post(18, "Carol", game_manager.get_player_group("Carol"))
posting_interface.like_post(20, "Dave", game_manager.get_player_group("Dave"))

game_manager.increment_round()
print("Scores at end of Round 4:", game_manager.get_scores_for_round(game_manager.get_round() - 1))