# Sandbox for data analysis
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def main():
    df = pd.read_parquet("linescores.parquet")
    df["hometeam_score"] = df["hometeam_line"].apply(sum)
    df["visteam_score"] = df["visteam_line"].apply(sum)
    # scores for use later
    # scores = df[['hometeam_score', 'visteam_score']].to_numpy()
    heatmap_data = pd.crosstab(df["visteam_score"], df["hometeam_score"])
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        heatmap_data,
        annot=True, fmt='d', cmap='YlOrRd', linewidths=0.5,
        xticklabels=True, yticklabels=True,
        cbar_kws={"label": "Number of Games"}
    )
    plt.title("Game Frequency by Score (Away x Home)")
    plt.xlabel("Home Team Runs")
    plt.ylabel("Away Team Runs")
    plt.tight_layout()
    plt.show()




if __name__ == "__main__":
    main()