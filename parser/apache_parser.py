import re
import pandas as pd

# Regex pattern for Apache combined log format
log_pattern = re.compile(
    r'(?P<ip>\S+) \S+ \S+ 

\[(?P<timestamp>.*?)\]

 "(?P<method>\S+) (?P<url>\S+) \S+" (?P<status>\d+) (?P<size>\S+) "(?P<referrer>.*?)" "(?P<user_agent>.*?)"'
)

def parse_apache_log(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    parsed_data = []
    for line in lines:
        match = log_pattern.match(line)
        if match:
            parsed_data.append(match.groupdict())

    df = pd.DataFrame(parsed_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d/%b/%Y:%H:%M:%S %z')
    return df

# Example usage
if __name__ == "__main__":
    df = parse_apache_log("data/apache_logs.txt")
    print(df.head())
