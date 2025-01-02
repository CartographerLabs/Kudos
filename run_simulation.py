from kudos.game_simulator import GameSimulator
from kudos.game_rules import game_rules

# Use the same network setup as test_game.py
social_network_groups = {
    "Casual users": "Regular social media users sharing daily content such as personal updates, entertainment, and general news. They engage in lighthearted interactions, follow popular trends, and contribute to the overall sense of community and normalcy within the platform.",
    "Far-right extremists": "Users with extreme political views that often promote nationalist, exclusionary, or anti-establishment ideologies. Their content may include inflammatory rhetoric, conspiracy-driven narratives, and the amplification of divisive topics, which can create tensions and conflict within the broader user base.",
    "Conspiracy theorists": "Users who believe in and propagate conspiracy theories, ranging from government cover-ups to secret societies and pseudoscientific claims. They frequently share speculative content and connect with like-minded individuals, fostering echo chambers that may challenge mainstream narratives and promote distrust in official sources.",
    "Political activists": "Users who are politically active and advocate for social, economic, or environmental causes - almost always right leaning on the political spectrum. They use the platform to organize events, raise awareness, and engage in debates. Their presence contributes to a dynamic environment, although at times, their passionate discourse can lead to heated exchanges or polarization."
}

social_network_biography = "The year is 2025. Social Network Z, a Twitter clone, has grown to host a diverse range of users. While the platform primarily consists of casual members sharing everyday content, it also attracts a smaller yet vocal minority of far-right extremists and conspiracy theorists. Originally envisioned as a digital 'Town Square' for free expression, the platform's reduced moderation staff has led to increased visibility of extreme content. This shift has transformed Social Network Z into a battleground for ideological expression, where the boundaries between free speech and harmful rhetoric are frequently tested."

# Create and run simulation
simulator = GameSimulator(
    network_groups=social_network_groups,
    network_biography=social_network_biography,
    game_rules=game_rules,
    num_ai_players=12
)

results = simulator.run_simulation(
    num_rounds=7,
    min_delay=0.5,
    max_delay=2.0,
    pause_between_rounds=False
)

print("\nSimulation Complete!")
print("Final Results:", results)
