import pandas as pd

def detect_bruteforce(df, threshold=5, window="1min"):
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="mixed", utc=True)
    df = df.sort_values("timestamp")
    
    # Check for failed login attempts - Apache 401/FAIL or SSH failed attempts
    failed = df[
        (pd.to_numeric(df["status"], errors="coerce") == 401) |
        (df["status"] == "FAIL") |
        (df["action"] == "Failed password for")
    ]
    if failed.empty:
        return pd.DataFrame()

    alerts = []

    for ip, group in failed.groupby("ip"):
        # Set timestamp as index for resampling
        group_indexed = group.set_index("timestamp")
        counts = group_indexed.resample(window).size()
        spikes = counts[counts >= threshold]

        for t, c in spikes.items():
            # Get all records in this time window
            window_start = t
            window_end = t + pd.Timedelta(window)
            window_data = group[(group["timestamp"] >= window_start) & (group["timestamp"] < window_end)]
            
            # Get unique sources for this window
            sources = window_data["source"].unique()
            source_str = ", ".join(sorted(sources))
            
            alerts.append({
                "ip": ip,
                "source": source_str,
                "time": t,
                "failed_attempts": c
            })

    return pd.DataFrame(alerts)


if __name__ == "__main__":
    apache = pd.read_csv("data/parsed_apache.csv")
    ssh = pd.read_csv("data/parsed_ssh.csv")

    df = pd.concat([apache, ssh], ignore_index=True)

    alerts = detect_bruteforce(df)
    alerts.to_csv("data/bruteforce_alerts.csv", index=False)

    print("✔ Alerts saved → data/bruteforce_alerts.csv")
    print(alerts)



