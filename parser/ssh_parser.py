# ssh_parser.py
import re
import pandas as pd
from datetime import datetime

# Matches lines like:
# Dec  2 02:12:55 server sshd[1245]: Failed password for root from 192.168.1.20 port 45322 ssh2
# Dec  2 02:12:59 server sshd[1245]: Accepted password for admin from 10.0.0.5 port 51432 ssh2
ssh_pattern = re.compile(
    r'^(?P<month>\w+)\s+(?P<day>\d+)\s+(?P<time>\d{2}:\d{2}:\d{2})\s+'
    r'(?P<host>\S+)\s+sshd\[\d+\]:\s+'
    r'(?P<action>Failed|Accepted)\s+password\s+for\s+(?:invalid user\s+)?(?P<user>\S+)\s+from\s+(?P<ip>\S+)'
)

MONTHS = {m: i+1 for i, m in enumerate(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])}

def parse_ssh_log(file_path="data/auth.log"):
    rows = []
    year = datetime.now().year

    with open(file_path, "r") as f:
        for line in f:
            m = ssh_pattern.match(line)
            if not m:
                continue
            d = m.groupdict()
            month = MONTHS.get(d['month'], 1)
            day = int(d['day'])
            ts_str = f"{year}-{month:02d}-{day:02d} {d['time']}"
            try:
                ts = pd.to_datetime(ts_str)
            except:
                ts = pd.NaT

            status = 401 if d['action'] == 'Failed' else 200

            rows.append({
                "timestamp": ts,
                "ip": d['ip'],
                "user": d['user'],
                "status": status,
                "source": "ssh"
            })

    df = pd.DataFrame(rows)
    if df.empty:
        print("⚠️ No SSH log entries parsed.")
        return df

    # ensure timestamp column exists and is datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df['status'] = pd.to_numeric(df['status'], errors='coerce').fillna(0).astype(int)

    # consistent columns
    cols = ['timestamp', 'ip', 'user', 'status', 'source']
    return df[cols]

if __name__ == "__main__":
    df = parse_ssh_log()
    if not df.empty:
        df.to_csv("data/parsed_ssh.csv", index=False)
        print("✅ Parsed SSH saved → data/parsed_ssh.csv")
        print(df.head())
