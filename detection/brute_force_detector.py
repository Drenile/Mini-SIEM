# brute_force_detection.py
import pandas as pd

def detect_brute_force(df, threshold=5, window="1min"):
    """
    Detect brute-force attempts across sources.
    Expects df to contain: timestamp, ip, status, source
    - For Apache: status==401 means failed login
    - For SSH: status==401 means failed login (we normalized in parser)
    Returns: DataFrame with columns: ip, source, time, failed_attempts
    """
    if df is None or df.empty:
        return pd.DataFrame(columns=["ip", "source", "time", "failed_attempts"])

    df = df.copy()

    # Normalize timestamp
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    # Drop rows without timestamp or ip
    df = df.dropna(subset=['timestamp', 'ip'])

    # Ensure status numeric
    if 'status' in df.columns:
        df['status'] = pd.to_numeric(df['status'], errors='coerce').fillna(0).astype(int)
    else:
        # If no status, assume non-failed
        df['status'] = 0

    # Ensure source column
    if 'source' not in df.columns:
        df['source'] = 'unknown'

    failed = df[df['status'] == 401].copy()
    if failed.empty:
        return pd.DataFrame(columns=["ip", "source", "time", "failed_attempts"])

    failed = failed.set_index('timestamp')

    alerts = []
    # group by both ip and source to differentiate apache vs ssh same IPs
    for (ip, source), group in failed.groupby(['ip', 'source']):
        counts = group.resample(window).size()
        suspicious = counts[counts > threshold]
        for ts, cnt in suspicious.items():
            alerts.append({
                "ip": ip,
                "source": source,
                "time": ts,
                "failed_attempts": int(cnt)
            })

    return pd.DataFrame(alerts)

if __name__ == "__main__":
    # quick manual test if CSVs exist
    try:
        a = pd.read_csv("data/parsed_apache.csv")
    except:
        a = pd.DataFrame()
    try:
        s = pd.read_csv("data/parsed_ssh.csv")
    except:
        s = pd.DataFrame()
    df = pd.concat([a, s], ignore_index=True) if not a.empty or not s.empty else pd.DataFrame()
    alerts = detect_brute_force(df)
    if not alerts.empty:
        alerts.to_csv("data/brute_force_alerts.csv", index=False)
        print("✅ Alerts saved → data/brute_force_alerts.csv")
        print(alerts)
    else:
        print("✅ No brute force alerts detected.")

