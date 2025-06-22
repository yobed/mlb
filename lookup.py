from numpy.linalg import norm
import numpy as np
import pandas as pd
import ast

class VectorLookup:
    def __init__(self, csv_file=None, parquet_file=None):
        if parquet_file:
            self.df = pd.read_parquet(parquet_file)
        elif csv_file:
            self.df = pd.read_csv(csv_file)
            self._preprocess_csv()
        else:
            raise ValueError("Must provide either a csv_file or parquet_file")

        self._convert_to_numpy()

    def _preprocess_csv(self):
        # convert string lists to actual Python lists
        self.df["visteam_line"] = self.df["visteam_line"].apply(ast.literal_eval)
        self.df["hometeam_line"] = self.df["hometeam_line"].apply(ast.literal_eval)
    
    def _convert_to_numpy(self):
        # make sure lists are NumPy arrays for cosine similarity
        self.df["visteam_line"] = self.df["visteam_line"].apply(np.array)
        self.df["hometeam_line"] = self.df["hometeam_line"].apply(np.array)

    def _cosine_sim(self, a, b):
        if len(a) != len(b):
            return 0 
        #a, b = np.array(a), np.array(b)
        if norm(a) == 0 or norm(b) == 0:
            return 0
        return np.dot(a, b) / (norm(a) * norm(b))


    def lookup(self, vector, top_k=5):
        # set vector as np array!!!
        vector = np.array(vector)
        # compute cosine similarity
        self.df["vis_sim"] = self.df["visteam_line"].apply(lambda x: self._cosine_sim(x, vector))
        self.df["home_sim"] = self.df["hometeam_line"].apply(lambda x: self._cosine_sim(x, vector))

        
        # combine into one DataFrame
        vis_matches = self.df[["game_id", "visteam", "hometeam", "visteam_line", "vis_sim"]].copy()
        vis_matches["team_type"] = "vis"
        vis_matches.rename(columns={"visteam_line": "line_score", "vis_sim": "similarity"}, inplace=True)

        home_matches = self.df[["game_id", "visteam", "hometeam", "hometeam_line", "home_sim"]].copy()
        home_matches["team_type"] = "home"
        home_matches.rename(columns={"hometeam_line": "line_score", "home_sim": "similarity"}, inplace=True)

        all_matches = pd.concat([vis_matches, home_matches])
        all_matches.sort_values("similarity", ascending=False, inplace=True)

        return all_matches.head(top_k)

