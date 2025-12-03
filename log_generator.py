import random
from datetime import datetime, timedelta

normal_ips = ["192.168.1.10", "192.168.1.20", "192.168.1.30"]
attacker_ips = ["10.0.0.5", "172.16.0.8"]

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "curl/7.68.0",
    "sqlmap/1.4.12",
    "Nmap Scripting Engine"
]

def generate_log(ip, ts, method, url, status, size, ref, ua):
    return f'{ip} - - [{ts}] "{method} {url} HTTP/1.1" {status} {size} "{ref}" "{ua}"'

def generate_logs(filename="data/apache_logs.txt", total_logs=500):
    now = datetime.now()
    logs = []

    for i in range(total_logs):
        timestamp = (now + timedelta(seconds=i)).strftime('%d/%b/%Y:%H:%M:%S -0700')

        ip = random.choice(normal_ips + attacker_ips)
        method = random.choice(["GET", "POST"])
        url = random.choice(["/index.html", "/login", "/admin", "/dashboard"])
        size = random.randint(100, 2000)
        referrer = "-"
        ua = random.choice(user_agents)

        # Base distribution
        status = random.choices(["200", "401", "403"], weights=[85, 10, 5])[0]

        # Brute-force injection (attackers hitting /login repeatedly)
        if ip in attacker_ips and url == "/login":
            if random.random() < 0.8:
                status = "401"

        logs.append(generate_log(ip, timestamp, method, url, status, size, referrer, ua))

    with open(filename, "w") as f:
        f.write("\n".join(logs))

    print(f"✅ Generated {total_logs} logs → {filename}")

if __name__ == "__main__":
    generate_logs()

import random
from datetime import datetime, timedelta

normal_ips = ["192.168.1.10", "192.168.1.20", "192.168.1.30"]
attacker_ips = ["10.0.0.5", "172.16.0.8"]

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "curl/7.68.0",
    "sqlmap/1.4.12",
    "Nmap Scripting Engine"
]

def generate_log(ip, ts, method, url, status, size, ref, ua):
    return f'{ip} - - [{ts}] "{method} {url} HTTP/1.1" {status} {size} "{ref}" "{ua}"'

def generate_logs(filename="data/apache_logs.txt", total_logs=500):
    now = datetime.now()
    logs = []

    for i in range(total_logs):
        timestamp = (now + timedelta(seconds=i)).strftime('%d/%b/%Y:%H:%M:%S -0700')

        ip = random.choice(normal_ips + attacker_ips)
        method = random.choice(["GET", "POST"])
        url = random.choice(["/index.html", "/login", "/admin", "/dashboard"])
        size = random.randint(100, 2000)
        referrer = "-"
        ua = random.choice(user_agents)

        # Base distribution
        status = random.choices(["200", "401", "403"], weights=[85, 10, 5])[0]

        # Brute-force injection (attackers hitting /login repeatedly)
        if ip in attacker_ips and url == "/login":
            if random.random() < 0.8:
                status = "401"

        logs.append(generate_log(ip, timestamp, method, url, status, size, referrer, ua))

    with open(filename, "w") as f:
        f.write("\n".join(logs))

    print(f"✅ Generated {total_logs} logs → {filename}")

if __name__ == "__main__":
    generate_logs()
