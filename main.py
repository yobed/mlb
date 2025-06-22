from lookup import VectorLookup 
from boxes_grab import BoxScoreProcess
import argparse


def main():
    parser = argparse.ArgumentParser(description="Look up similar line scores from box score data")
    parser.add_argument("-d", "--debug", action="store_true", help="Run in debug mode (one file only)")
    parser.add_argument("-s", "--save", action="store_true", help="Save to file (csv)")
    parser.add_argument("-v", "--vector", nargs="+", type=int, required=True, help="Line score vector to compare (e.g. -v 0 0 0 0 0 1 1 0 4)")
    parser.add_argument("-k", "--top_k", type=int, default=5, help="Number of top matches to return")
    args = parser.parse_args()
    if (args.vector):
        print(f"Target vector: {args.vector}")
        lookup = VectorLookup(parquet_file="linescores.parquet")
        results = lookup.lookup(vector=args.vector, top_k=args.top_k)
        print(results)
        if args.save:
            results.to_csv("vector_matches.csv", index=False)

    


if __name__ == "__main__":
    main()
    

