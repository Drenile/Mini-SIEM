
# log_generator.py
import random
from datetime import datetime, timedelta

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# --- IPs & user agents ---
normal_ips = ["192.168.1.10", "192.168.1.20", "192.168.1.30"]
attacker_ips = ["10.0.0.5", "172.16.0.8"]

apache_user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "curl/7.68.0",
    "sqlmap/1.4.12",
    "Nmap Scripting Engine"
]

ssh_users = ["root", "admin", "ubuntu", "service", "test"]

# --- Apache generator ---
def _generate_apache_line(ip, timestamp, method, url, status, size, referrer, ua):
    return f'{ip} - - [{timestamp}] "{method} {url} HTTP/1.1" {status} {size} "{referrer}" "{ua}"'

def generate_apache_logs(filename="data/apache_logs.txt", total_logs=500):
    now = datetime.now()
    lines = []

    for i in range(total_logs):
        ts = (now + timedelta(seconds=i)).strftime('%d/%b/%Y:%H:%M:%S -0700')  # keep previous -0700 format
        ip = random.choice(normal_ips + attacker_ips)
        method = random.choice(["GET", "POST"])
        url = random.choice(["/index.html", "/login", "/admin", "/dashboard"])
        size = random.randint(100, 2000)
        referrer = "-"
        ua = random.choice(apache_user_agents)
        status = random.choices(["200", "401", "403"], weights=[85, 10, 5])[0]

        # If attacker hitting /login, increase probability of 401
        if ip in attacker_ips and url == "/login" and random.random() < 0.8:
            status = "401"

        lines.append(_generate_apache_line(ip, ts, method, url, status, size, referrer, ua))

    with open(filename, "w") as f:
        f.write("\n".join(lines))

    print(f"✅ Generated {total_logs} Apache logs → {filename}")

# --- SSH generator ---
def _generate_ssh_line(ip, user, action, timestamp):
    month = MONTHS[timestamp.month - 1]
    day = timestamp.day
    time_str = timestamp.strftime("%H:%M:%S")
    return (
        f"{month} {day:2d} {time_str} server sshd[1234]: "
        f"{action} password for {user} from {ip} port {random.randint(20000, 60000)} ssh2"
    )

def generate_ssh_logs(filename="data/auth.log", total_logs=500):
    now = datetime.now()
    lines = []

    for i in range(total_logs):
        ip = random.choice(normal_ips + attacker_ips)
        user = random.choice(ssh_users)
        ts = now + timedelta(seconds=i)
        if ip in attacker_ips:
            action = random.choices(["Failed", "Accepted"], weights=[95, 5])[0]
        else:
            action = random.choices(["Accepted", "Failed"], weights=[85, 15])[0]
        lines.append(_generate_ssh_line(ip, user, action, ts))

    # add an explicit brute-force burst from one attacker
    attacker = random.choice(attacker_ips)
    burst_start = now + timedelta(seconds=total_logs + 1)
    for i in range(15):
        lines.append(_generate_ssh_line(attacker, "root", "Failed", burst_start + timedelta(seconds=i)))

    with open(filename, "w") as f:
        f.write("\n".join(lines))

    print(f"✅ Generated {len(lines)} SSH logs → {filename}")

# --- Combined helper ---
def generate_all_logs(apache_file="data/apache_logs.txt", ssh_file="data/auth.log",
                      apache_count=500, ssh_count=500):
    generate_apache_logs(filename=apache_file, total_logs=apache_count)
    generate_ssh_logs(filename=ssh_file, total_logs=ssh_count)
    print("✅ Generated both Apache and SSH logs.")

if __name__ == "__main__":
    generate_all_logs()
