import random
from datetime import datetime, timedelta

# Sample IPs and user agents
normal_ips = ["192.168.1.10", "192.168.1.20", "192.168.1.30"]
attacker_ips = ["10.0.0.5", "172.16.0.8"]
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "curl/7.68.0",
    "sqlmap/1.4.12",
    "Nmap Scripting Engine"
]

# Apache log format template
def generate_log(ip, timestamp, method, url, status, size, referrer, user_agent):
    return f'{ip} - - [{timestamp}] "{method} {url} HTTP/1.1" {status} {size} "{referrer}" "{user_agent}"'

# Generate logs
def generate_logs(filename="data/apache_logs.txt", total_logs=500):
    now = datetime.now()
    logs = []

    for _ in range(total_logs):
        ip = random.choice(normal_ips + attacker_ips)
        timestamp = (now + timedelta(seconds=random.randint(0, 3600))).strftime('%d/%b/%Y:%H:%M:%S -0700')
        method = random.choice(["GET", "POST"])
        url = random.choice(["/index.html", "/login", "/admin", "/dashboard"])
        status = random.choices(["200", "401", "403"], weights=[80, 15, 5])[0]
        size = random.randint(200, 1500)
        referrer = "-"
        user_agent = random.choice(user_agents)

        # Inject brute-force behavior
        if ip in attacker_ips and url == "/login":
            status = "401"  # failed login

        log_entry = generate_log(ip, timestamp, method, url, status, size, referrer, user_agent)
        logs.append(log_entry)

    # Write to file
    with open(filename, "w") as f:
        for log in logs:
            f.write(log + "\n")

    print(f"Generated {total_logs} logs in {filename}")

# Run generator
if __name__ == "__main__":
    generate_logs()
