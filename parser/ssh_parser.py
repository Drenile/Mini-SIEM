import re
import pandas as pd

ssh_pattern = re.compile(
    r'^(?P<timestamp>\S+ \S+)\s+\S+\s+sshd\[\d+\]:\s+'
    r'(?P<action>Failed password for|Accepted password for)\s+'
    r'(?:invalid user\s+)?(?P<user>\S+)\s+from\s+(?P<ip>\S+)\s+port\s+(?P<port>\d+)\s+ssh2'
)

def parse_ssh_log(file_path):
    parsed = []

    with open(file_path, "r") as f:
        for line in f:
            m = ssh_pattern.match(line.strip())
            if m:
                parsed.append(m.groupdict())
            else:
                print("NO MATCH:", line)

    df = pd.DataFrame(parsed)

    if df.empty:
        print("⚠ WARNING: SSH log parser found ZERO matches")

    df["source"] = "ssh"
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="mixed", utc=True)
    return df

if __name__ == "__main__":
    df = parse_ssh_log("data/ssh_logs.txt")
    df.to_csv("data/parsed_ssh.csv", index=False)
    print("✔ SSH logs parsed → data/parsed_ssh.csv")
    print(df.head())

