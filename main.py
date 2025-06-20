import os
import glob
import chromadb
import pprint
import argparse

class BoxScoreProcess:

    def __init__(self, files, collection, debug):
        self.collection = collection
        self.files = files
        self._lines = None
        self._debug = debug

    def run(self):
        self._lines = self._process_files(eba_files=self.files, DEBUG_ONE=self._debug)
        # Only call process_lines
        self._process_lines(self._lines)

    def _process_files(self, eba_files, DEBUG_ONE):
        if DEBUG_ONE:
            with open(eba_files[0], 'r') as f:
                lines = f.readlines()
            return lines
        else:
            all_lines = []
            for file in eba_files:
                with open(file, 'r') as f:
                    lines = f.readlines()
                    all_lines.append(lines)
            return all_lines

    def _process_game(self, info, line_scores, game_id):
        metadata = {}
        embeddings = []
        metadata["game_id"] = game_id
        
        visteam = info.get("visteam")
        hometeam = info.get("hometeam")
        date = info.get("date")
        site = info.get("site")
        innings_played = 9
        game = {
            "game_id": game_id,
            "date": date,
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
            


def main():
    parser = argparse.ArgumentParser(description="Parse EBA box scores and store in ChromaDB")
    parser.add_argument("-d", "--debug", action="store_true", help="Run in debug mode (one file only)")
    args = parser.parse_args()

    client = chromadb.PersistentClient(path="./mlb_box_scores")
    collection = client.get_or_create_collection("box_scores")

    eba_files = glob.glob("./boxes/*.EBA")
    processor = BoxScoreProcess(eba_files, collection, debug=args.debug)
    processor.run()

if __name__ == "__main__":
    main()
        