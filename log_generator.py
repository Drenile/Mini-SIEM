import random
from datetime import datetime, timedelta

# -----------------------------
# APACHE LOG GENERATION
# -----------------------------

normal_ips = ["192.168.1.10", "192.168.1.20", "192.168.1.30"]
attacker_ips = ["10.0.0.5", "172.16.0.8"]

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "curl/7.68.0",
    "sqlmap/1.4.12",
    "Nmap Scripting Engine"
]

def generate_apache_log(ip, timestamp, method, url, status, size, referrer, user_agent):
    return f'{ip} - - [{timestamp}] "{method} {url} HTTP/1.1" {status} {size} "{referrer}" "{user_agent}"'

def generate_apache_logs(filename="data/apache_logs.txt", total_logs=500):
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

        # Inject brute force for Apache attackers
        if ip in attacker_ips and url == "/login":
            status = "401"

        logs.append(generate_apache_log(ip, timestamp, method, url, status, size, referrer, user_agent))

    with open(filename, "w") as f:
        f.write("\n".join(logs) + "\n")

    print(f"✔ Generated {total_logs} Apache logs → {filename}")


# -----------------------------
# APACHE BRUTE FORCE BURST
# -----------------------------

def generate_apache_burst(filename="data/apache_logs.txt", ip="10.0.0.5", attempts=20):
    now = datetime.now()
    logs = []

    for i in range(attempts):
        timestamp = (now + timedelta(seconds=i)).strftime('%d/%b/%Y:%H:%M:%S -0700')
        logs.append(
            f'{ip} - - [{timestamp}] "POST /login HTTP/1.1" 401 512 "-" "curl/7.68"'
        )

    with open(filename, "a") as f:
        f.write("\n".join(logs) + "\n")

    print(f"🔥 Injected {attempts} Apache brute-force attempts for {ip}")


# -----------------------------
# SSH LOG GENERATION
# -----------------------------

ssh_users = ["root", "admin", "test", "ubuntu", "guest"]

def generate_ssh_logs(filename="data/ssh_logs.txt", total_logs=500):
    now = datetime.now()
    logs = []

    for _ in range(total_logs):
        ip = random.choice(normal_ips + attacker_ips)
        timestamp = (now + timedelta(seconds=random.randint(0, 3600))).strftime('%Y-%m-%d %H:%M:%S')

        if ip in attacker_ips:
            # Failed password burst
            log = (
                f"{timestamp} server1 sshd[1234]: Failed password for invalid user "
                f"{random.choice(ssh_users)} from {ip} port {random.randint(30000, 60000)} ssh2"
            )
        else:
            # Normal "Accepted password"
            log = (
                f"{timestamp} server1 sshd[1234]: Accepted password for {random.choice(ssh_users)} "
                f"from {ip} port {random.randint(30000, 60000)} ssh2"
            )

        logs.append(log)

    with open(filename, "w") as f:
        f.write("\n".join(logs) + "\n")

    print(f"✔ Generated {total_logs} SSH logs → {filename}")


# -----------------------------
# SSH BRUTE FORCE BURST
# -----------------------------

def generate_ssh_burst(filename="data/ssh_logs.txt", ip="10.0.0.5", attempts=30):
    now = datetime.now()
    logs = []

    for i in range(attempts):
        timestamp = (now + timedelta(seconds=i)).strftime('%Y-%m-%d %H:%M:%S')
        logs.append(
            f"{timestamp} server1 sshd[9999]: Failed password for root from {ip} port 40000 ssh2"
        )

    with open(filename, "a") as f:
        f.write("\n".join(logs) + "\n")

    print(f"🔥 Injected {attempts} SSH brute-force attempts for {ip}")


# -----------------------------
# MAIN GENERATOR ENTRYPOINT
# -----------------------------

if __name__ == "__main__":
    generate_apache_logs()
    generate_ssh_logs()

    # Uncomment to create burst attacks:
    generate_apache_burst(ip="10.0.0.5", attempts=30)
    generate_ssh_burst(ip="10.0.0.5", attempts=50)


