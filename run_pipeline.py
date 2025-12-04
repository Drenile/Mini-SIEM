# run_pipeline.py
import pandas as pd
from parser.apache_parser import parse_apache_log
from parser.ssh_parser import parse_ssh_log
from detection.brute_force_detector import detect_bruteforce

def main():
    print("\n🚀 Running SIEM pipeline (Apache + SSH)\n")

    # --- Parse Apache logs if available ---
    try:
        a = parse_apache_log("data/apache_logs.txt")
        if not a.empty:
            a.to_csv("data/parsed_apache.csv", index=False)
            print(f"📄 Parsed Apache -> data/parsed_apache.csv ({len(a)} rows)")
        else:
            print("⚠️ Apache parser found 0 rows.")
    except FileNotFoundError:
        print("⚠️ Apache raw log (data/apache_logs.txt) not found. Run log_generator.generate_apache_logs()")

    # --- Parse SSH logs if available ---
    try:
        s = parse_ssh_log("data/ssh_logs.txt")
        if not s.empty:
            s.to_csv("data/parsed_ssh.csv", index=False)
            print(f"📄 Parsed SSH -> data/parsed_ssh.csv ({len(s)} rows)")
        else:
            print("⚠️ SSH parser found 0 rows.")
    except FileNotFoundError:
        print("⚠️ SSH raw log (data/ssh_logs.txt) not found. Run log_generator.generate_ssh_logs()")

    # --- Load parsed files (if present) ---
    parsed_list = []
    try:
        parsed_apache = pd.read_csv("data/parsed_apache.csv")
        parsed_list.append(parsed_apache)
    except:
        parsed_apache = pd.DataFrame()

    try:
        parsed_ssh = pd.read_csv("data/parsed_ssh.csv")
        parsed_list.append(parsed_ssh)
    except:
        parsed_ssh = pd.DataFrame()

    if not parsed_list:
        print("\n❌ No parsed sources available. Exiting.")
        return

    combined = pd.concat(parsed_list, ignore_index=True, sort=False)
    print(f"\n🔎 Running brute-force detection on {len(combined)} combined rows...")
    alerts = detect_bruteforce(combined)

    if alerts.empty:
        print("✅ No brute-force alerts detected.")
    else:
        alerts.to_csv("data/brute_force_alerts.csv", index=False)
        print(f"🚨 Alerts saved -> data/brute_force_alerts.csv ({len(alerts)} rows)")
        print(alerts)

if __name__ == "__main__":
    main()

