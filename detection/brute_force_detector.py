import pandas as pd

def detect_brute_force(df, threshold=5, window='1min'):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)

    grouped = df[df['status'] == '401'].groupby('ip')
    alerts = []

    for ip, group in grouped:
        counts = group.resample(window).size()
        suspicious = counts[counts > threshold]
        for time, count in suspicious.items():
            alerts.append({
                'ip': ip,
                'time': time,
                'failed_attempts': count
            })

    return pd.DataFrame(alerts)

# Example usage
if __name__ == "__main__":
    logs = pd.read_csv("data/parsed_apache.csv")
    alerts = detect_brute_force(logs)
    print(alerts)
