# apache_parser.py
import re
import pandas as pd

log_pattern = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ '
    r'\[(?P<timestamp>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<url>\S+) (?P<protocol>\S+)" '
    r'(?P<status>\d{3}) (?P<size>\S+) '
    r'"(?P<referrer>[^"]*)" "(?P<user_agent>[^"]*)"'
)

def parse_apache_log(file_path="data/apache_logs.txt", debug=False):
    parsed = []
    with open(file_path, "r") as f:
        for line in f:
            m = log_pattern.match(line)
            if m:
                d = m.groupdict()
                d['source'] = 'apache'
                parsed.append(d)
            elif debug:
                print("NO MATCH (apache):", line.strip())

    df = pd.DataFrame(parsed)
    if df.empty:
        print("⚠️ No Apache log entries parsed.")
        return df

    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d/%b/%Y:%H:%M:%S %z', errors='coerce')
    df['status'] = pd.to_numeric(df['status'], errors='coerce').fillna(0).astype(int)
    df['size'] = pd.to_numeric(df['size'], errors='coerce').fillna(0).astype(int)

    # keep consistent column order
    cols = ['timestamp', 'ip', 'method', 'url', 'protocol', 'status', 'size', 'referrer', 'user_agent', 'source']
    cols = [c for c in cols if c in df.columns]
    return df[cols]

if __name__ == "__main__":
    df = parse_apache_log()
    if not df.empty:
        df.to_csv("data/parsed_apache.csv", index=False)
        print("✅ Parsed Apache saved → data/parsed_apache.csv")
        print(df.head())

