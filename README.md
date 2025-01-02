# Influence 

This simulation leverages LLMs to model a social media network, complete with user groups, generated posts, and a scoring system.

## ✨ Purpose of the Simulation
The goal is to illustrate how different groups can influence an online community by sharing or reacting to posts. Points are awarded based on interactions, and alignment with the group's ideological slant.

## 🚀 Getting Started
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. (Optional) Install as a package:
   ```
   pip install .
   ```
3. Run the simulation:
   ```
   python run_simulation.py
   ```

## 🗂️ Project Structure
- `game/`: Core simulation logic (scoring, posting, AI integration, etc.)  
- `run_simulation.py`: Entry point for running the simulation  
- `requirements.txt`: Lists required packages  
- `setup.py`: Installation script  
- `README.md`: You're reading it now!  

## 🔗 How It Works
1. User groups share, like, and reply to posts.  
2. The scoring system rewards (or penalizes) behaviors based on alignment with group goals.  
3. The simulation runs for a set number of rounds, and the winning group emerges based on total points.