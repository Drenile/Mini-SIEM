import re
import pandas as pd

# Apache combined log format regex
log_pattern = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ '
    r'\[(?P<timestamp>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<url>\S+) (?P<protocol>\S+)" '
    r'(?P<status>\d{3}) (?P<size>\S+) '
    r'"(?P<referrer>[^"]*)" "(?P<user_agent>[^"]*)"'
)

def parse_apache_log(file_path, debug=False):
    """Parses an Apache log file into a structured DataFrame."""

    parsed_data = []

    with open(file_path, 'r') as f:
        for line in f:
            match = log_pattern.match(line)
            if match:
                parsed_data.append(match.groupdict())
            elif debug:
                print("NO MATCH:", line.strip())

    df = pd.DataFrame(parsed_data)

    if df.empty:
        print("⚠️ No valid log entries found. Check regex or log format.")
        return df

    # Convert fields
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%d/%b/%Y:%H:%M:%S %z")
    df["status"] = df["status"].astype(int)
    df["size"] = df["size"].astype(int)

    return df

if __name__ == "__main__":
    df = parse_apache_log("data/apache_logs.txt")
    df.to_csv("data/parsed_apache.csv", index=False)
    print("✅ Parsed logs saved to data/parsed_apache.csv")
    print(df.head())
