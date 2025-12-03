import pandas as pd
from detection.brute_force_detector import detect_brute_force

def main():
    print("\n🚀 Starting detection pipeline...\n")

    # Load parsed logs
    try:
        df = pd.read_csv("data/parsed_apache.csv")
    except FileNotFoundError:
        print("❌ ERROR: parsed_apache.csv not found.")
        print("Run apache_parser.py first.")
        return

    print(f"📄 Loaded {len(df)} parsed log entries.\n")

    # ----------------------
    # 1. Brute Force Detector
    # ----------------------
    print("🔎 Running brute-force detection...")
    alerts = detect_brute_force(df)

    if alerts.empty:
        print("✅ No brute-force attacks detected.\n")
    else:
        print("🚨 Brute-force attacks found:")
        print(alerts.to_string(index=False))
        print()

    print("🎉 Pipeline finished.\n")

if __name__ == "__main__":
    main()
