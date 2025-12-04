import re
import pandas as pd

log_pattern = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ '
    r'\[(?P<timestamp>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<url>\S+) (?P<protocol>\S+)" '
    r'(?P<status>\d{3}) (?P<size>\S+) '
    r'"(?P<referrer>[^"]*)" "(?P<user_agent>[^"]*)"'
)

def parse_apache_log(filepath="data/apache_logs.txt"):
    parsed = []
    with open(filepath) as f:
        for line in f:
            m = log_pattern.match(line)
            if m:
                d = m.groupdict()
                d["source"] = "apache"
                parsed.append(d)

    df = pd.DataFrame(parsed)
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%d/%b/%Y:%H:%M:%S %z")

    df.to_csv("data/parsed_apache.csv", index=False)
    print("✔ Saved parsed Apache logs → data/parsed_apache.csv")
    return df


if __name__ == "__main__":
    parse_apache_log()


