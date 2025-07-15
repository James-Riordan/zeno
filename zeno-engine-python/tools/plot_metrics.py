import pandas as pd
import argparse

def print_metrics(csv_path: str) -> None:
    df = pd.read_csv(csv_path)
    print(f"\n📊 Metrics Summary from: {csv_path}")
    print(df.describe(include='all'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="Path to metrics CSV")
    args = parser.parse_args()

    print_metrics(args.csv)
