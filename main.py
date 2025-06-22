import os
import glob
import chromadb
import pprint
import argparse
import pandas as pd

class BoxScoreProcess:

    def __init__(self, files, collection, debug):
        self.collection = collection
        self.files = files
        #self._lines = None
        if debug:
            self.files = [self.files[0]]
        self.games = []

    def run(self):
        for file in self.files:
            try:
                lines = self._process_file(file_path=file)
                self._process_lines(lines)
            except Exception as e:
                print(f"Error in file: {file}")
                print(e)


    def _process_file(self, file_path):
        with open(file_path, 'r') as f:
            return f.readlines()


    def _process_game(self, info, line_scores, game_id):
        metadata = {}
        metadata["game_id"] = game_id
        
        visteam = info.get("visteam")
        hometeam = info.get("hometeam")
        date = info.get("date")
        site = info.get("site")
        innings_played = 9
        game = {
            "date": date,
            "game_id": game_id,
            "site": site,
            "hometeam": hometeam,
            "visteam": visteam,
            "innings": innings_played,
            "hometeam_line": [],
            "visteam_line": [],
        }
    
        # Line Scores
        for line in line_scores: # 2 box scores
            parts = line.strip().split(",")
            team_index = int(parts[1])
            scores = list(map(int, parts[2:]))
            innings_played = len(scores)
            team = visteam if team_index == 0 else hometeam
            print(team, scores)
            if team_index == 0:
                game["visteam_line"] = scores
            else:
                game["hometeam_line"] = scores
        pprint.pprint(game)
        self.games.append(game)

        
        
            
            
            

    def _process_lines(self, lines):
        info = {}
        line_scores = []
        game_id = None
        for line in lines:
            #print(line)
            if line.startswith("id,"): # Start of game
                if game_id is not None:
                    self._process_game(info, line_scores, game_id)
                # Reset everything
                info = {}
                line_scores = []
                game_id = line.strip().split(",")[1]
            elif line.startswith("info,"):
                parts = line.strip().split(",")
                info[parts[1]] = parts[2]

            elif line.startswith("line"):
                line_scores.append(line)
        # get last game
        if game_id is not None:
            self._process_game(info, line_scores, game_id)
    def get_dataframe(self):
        df = pd.DataFrame(self.games)
        df["date"] = pd.to_datetime(df["date"], format="%Y/%m/%d")
        df.set_index("date", inplace=True)
        return df
            


def main():
    parser = argparse.ArgumentParser(description="Parse EBA box scores and store in ChromaDB")
    parser.add_argument("-d", "--debug", action="store_true", help="Run in debug mode (one file only)")
    parser.add_argument("-s", "--save", action="store_true", help="Save to file (csv)")
    args = parser.parse_args()

    client = chromadb.PersistentClient(path="./mlb_box_scores")
    collection = client.get_or_create_collection("box_scores")

    e_files = glob.glob("./boxes/*")
    processor = BoxScoreProcess(e_files, collection, debug=args.debug)
    processor.run()
    df = processor.get_dataframe()
    print(df)
    if (args.save):
        df.to_csv("linescores.csv")
    

if __name__ == "__main__":
    main()
        