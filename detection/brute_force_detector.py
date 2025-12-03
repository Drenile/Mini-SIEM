import pandas as pd

def detect_brute_force(df, threshold=5, window="1min"):
    """Detects brute-force attacks based on repeated 401 responses."""

    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["status"] = df["status"].astype(int)

    df = df.set_index("timestamp")

    failed = df[df["status"] == 401]

    if failed.empty:
        print("⚠️ No failed login attempts (401) found.")
        return pd.DataFrame()

    alerts = []

    for ip, group in failed.groupby("ip"):
        counts = group.resample(window).size()
        suspicious = counts[counts > threshold]

        for time, count in suspicious.items():
            alerts.append({
                "ip": ip,
                "time": time,
                "failed_attempts": count
            })

    return pd.DataFrame(alerts)

if __name__ == "__main__":
    logs = pd.read_csv("data/parsed_apache.csv")
    alerts = detect_brute_force(logs)

    alerts.to_csv("data/brute_force_alerts.csv", index=False)
    print("✅ Alerts saved to data/brute_force_alerts.csv")
    print(alerts)
