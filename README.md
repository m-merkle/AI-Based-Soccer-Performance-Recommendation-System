# AI-Based Soccer Performance Recommendation System
## Key Points
- Model uses KMeans++ clustering and Random Forest classification to group players and suggest drills for performance improvement
- User-friendly GUI with Python (Tkinter) created for coaches to easily upload datasets, view player clusters, and access drill recommendations
- Refined using the University of North Alabama's womens soccer data from 2023 - 2024
## Project Overview
My project, the soccer performance recommendation system, utilizes artificial intelligence to recommend performance improvements for soccer players and how to achieve those improvements. This system came about due to the rising prevalence of tracking systems in soccer specifically, which provides coaches with extensive data on player performance during games and practices. The system allows users to analyze this data by exporting game metrics for players and inputting them into the system, following the format of the provided example game data file.

There are two main stages to the system.
- First, the system groups players using clustering based on a user-provided dataset.
- Then, a random forest classifier, trained on labeled game data from the 2023 UNA soccer season, predicts the recommended class (category) of soccer drills for each cluster.

Ultimately, the system displays the players in each cluster, the recommended drill category, and a description of the category recommended. This system offers coaches and players tailored drill recommendations to improve performance and will hopefully allow tracking data to be more beneficial to soccer teams.


