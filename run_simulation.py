from kudos.game_simulator import GameSimulator
from kudos.game_rules import game_rules

# Use the same network setup as test_game.py
social_network_groups = {
    "Casual users": """Regular social media users who share daily content such as personal updates, entertainment, and general news. They engage in lighthearted interactions, follow popular trends, and contribute to the overall sense of community and normalcy within the platform.
    Content Examples:
    - Photos from family gatherings, vacation snapshots.
    - Sharing viral videos or memes.
    - Participating in trending challenges.
    - Commenting on popular culture events like movie releases or sports games.""",

    "Far-right extremists": """Users with extreme political views that often promote nationalist, exclusionary, or anti-establishment ideologies. Their content may include inflammatory rhetoric, conspiracy-driven narratives, and the amplification of divisive topics, which can create tensions and conflict within the broader user base.
    Content Examples:
    - Posts promoting white supremacist ideologies.
    - Sharing anti-immigrant propaganda.
    - Disseminating conspiracy theories like QAnon.
    - Using coded language or symbols associated with hate groups.""",

    "Conspiracy theorists": """Users who believe in and propagate conspiracy theories, ranging from government cover-ups to secret societies and pseudoscientific claims. They frequently share speculative content and connect with like-minded individuals, fostering echo chambers that may challenge mainstream narratives and promote distrust in official sources.
    Content Examples:
    - Claims about the moon landing being faked.
    - Anti-vaccine misinformation.
    - Theories about 5G technology causing health issues.
    - Assertions that certain global events are orchestrated by secret elites.""",

    "Political activists": """Users who are politically active and advocate for social, economic, or environmental causes. They use the platform to organize events, raise awareness, and engage in debates. Their presence contributes to a dynamic environment, although at times, their passionate discourse can lead to heated exchanges or polarization.
    Content Examples:
    - Campaigning for climate change action.
    - Promoting social justice movements like Black Lives Matter.
    - Organizing protests or rallies.
    - Sharing petitions or fundraising for political causes.""",

    "Misinformation spreaders": """Users who, intentionally or unintentionally, share false or misleading information. This can range from health-related myths to fabricated news stories, contributing to public confusion and mistrust.
    Content Examples:
    - Sharing fake news articles.
    - Promoting miracle cures without scientific backing.
    - Spreading rumors during crises.
    - Misrepresenting statistical data.""",

    "Trolls and harassers": """Individuals who deliberately provoke or harass others online to elicit reactions or cause distress. Their behavior can disrupt conversations and create a hostile environment.
    Content Examples:
    - Posting inflammatory comments.
    - Engaging in targeted harassment or doxing.
    - Creating offensive memes aimed at individuals or groups.
    - Coordinating online attacks.""",

    "Commercial spammers": """Accounts primarily focused on promoting products or services, often without regard for platform rules or user experience. Their activities can clutter feeds and annoy users.
    Content Examples:
    - Posting repetitive advertisements.
    - Sharing links to dubious products.
    - Using clickbait titles to drive traffic.
    - Sending unsolicited promotional messages.""",

    "Memers and content creators": """Users who create and share original content, including memes, videos, art, and writing. They contribute to the platform's culture and can influence trends and discussions.
    Content Examples:
    - Developing viral memes.
    - Producing educational videos.
    - Sharing digital artwork.
    - Writing insightful blog posts or threads."""
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
