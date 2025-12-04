# Mini-SIEM

A lightweight SIEM system that parses Apache and SSH logs, detects brute-force attacks, and visualizes security threats.

## Quick Features

- Dual log parsing (Apache + SSH)
- Brute-force detection (5+ failed attempts/min)
- Interactive dashboard (Plotly/Dash)
- Cross-service correlation

## Project Structure

```
Mini-SIEM/
├── data/
│   ├── apache_logs.txt          # Raw Apache access logs
│   ├── ssh_logs.txt             # Raw SSH authentication logs
│   ├── parsed_apache.csv        # Parsed Apache data
│   ├── parsed_ssh.csv           # Parsed SSH data
│   └── brute_force_alerts.csv   # Detected attacks
├── parser/
│   ├── apache_parser.py         # Apache log parser
│   └── ssh_parser.py            # SSH log parser
├── detection/
│   └── brute_force_detector.py  # Attack detection engine
├── run_pipeline.py              # End-to-end pipeline
├── dashboard.py                 # Interactive Dash visualization
├── log_generator.py             # Generate synthetic logs
└── README.md                    # This file
```

## Installation

### Requirements
- Python 3.8+
- pandas
- plotly
- dash

### Setup

```bash
# Clone the repository
git clone https://github.com/Drenile/Mini-SIEM.git
cd Mini-SIEM

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### TL;DR - Quick Commands

```bash
# Get started in 3 commands:
pip install -r requirements.txt
python run_pipeline.py              # Run detection
python dashboard.py                  # View results at http://127.0.0.1:8050/
```

### Option 1: Full Pipeline (Recommended for Portfolio)

Run the complete SIEM pipeline in one command:

```bash
python run_pipeline.py
```

This will:
1. Parse Apache logs from `data/apache_logs.txt`
2. Parse SSH logs from `data/ssh_logs.txt`
3. Detect brute-force attacks
4. Generate `data/brute_force_alerts.csv`

**Example Output:**
```
Running SIEM pipeline (Apache + SSH)

Saved parsed Apache logs → data/parsed_apache.csv
Parsed Apache -> data/parsed_apache.csv (530 rows)
Parsed SSH -> data/parsed_ssh.csv (550 rows)

Running brute-force detection on 1080 combined rows...
Alerts saved -> data/brute_force_alerts.csv (6 rows)
```

### Option 2: Interactive Dashboard

View real-time threat visualization:

```bash
python dashboard.py
```

Then open your browser to: **http://127.0.0.1:8050/**

The dashboard displays:
- Request volume over time
- Status code distribution by source
- Detected brute-force attacks with IP addresses

### Option 3: Step-by-Step Processing

Parse individual log sources:

```bash
# Parse Apache logs
python parser/apache_parser.py
# Output: data/parsed_apache.csv

# Parse SSH logs
python parser/ssh_parser.py
# Output: data/parsed_ssh.csv

# Run detection on parsed logs
python detection/brute_force_detector.py
# Output: data/bruteforce_alerts.csv
```

## Sample Data

The repository includes sample log files with realistic brute-force attack patterns:

```bash
# View sample results
cat data/brute_force_alerts.csv
```

Expected output (6 attacks detected):
```
ip,source,time,failed_attempts
10.0.0.5,ssh,2025-12-04 00:21:00+00:00,11
10.0.0.5,ssh,2025-12-04 00:22:00+00:00,43
10.0.0.5,ssh,2025-12-04 00:26:00+00:00,6
10.0.0.5,ssh,2025-12-04 01:03:00+00:00,5
10.0.0.5,apache,2025-12-04 07:21:00+00:00,10
10.0.0.5,apache,2025-12-04 07:22:00+00:00,22
```

## Portfolio Highlights

This project demonstrates key cybersecurity and software engineering skills:

**Security Skills:**
- Log analysis and parsing
- Threat detection algorithm design
- Multi-source attack correlation
- Real-time security monitoring

**Software Engineering:**
- Data processing pipeline (pandas)
- Interactive web visualization (Dash/Plotly)
- Modular code architecture
- Error handling and data validation
- CSV data formats and parsing

**Technologies Used:**
- Python (core language)
- Pandas (data manipulation)
- Plotly/Dash (visualization)
- Regex (log parsing)
- Git (version control)

## Usage

## Alert Output

The system generates alerts in `data/brute_force_alerts.csv`:

| ip | source | time | failed_attempts |
|---|---|---|---|
| 10.0.0.5 | ssh | 2025-12-04 00:21:00+00:00 | 11 |
| 10.0.0.5 | ssh | 2025-12-04 00:22:00+00:00 | 43 |
| 10.0.0.5 | apache | 2025-12-04 07:21:00+00:00 | 10 |

**Alert Interpretation:**
- **ip**: Source IP of the attacker
- **source**: Service under attack (ssh or apache)
- **time**: Time window of the attack (rounded to minute)
- **failed_attempts**: Number of failed attempts in that window

## Configuration

### Detection Threshold

Modify the threshold in `detection/brute_force_detector.py`:

```python
# Default: 5 failed attempts per minute
alerts = detect_bruteforce(df, threshold=5, window="1min")

# Custom: 10 attempts per 5 minutes
alerts = detect_bruteforce(df, threshold=10, window="5min")
```

### Log Paths

Update file paths in `run_pipeline.py`:
```python
a = parse_apache_log("path/to/apache_logs.txt")
s = parse_ssh_log("path/to/ssh_logs.txt")
```

## Data Flow

```
Raw Logs
  ↓
┌─────────────────┬──────────────────┐
│ Apache Parser   │ SSH Parser       │
└─────────────────┴──────────────────┘
  ↓                ↓
parsed_apache.csv  parsed_ssh.csv
  ↓                ↓
  └────────┬───────┘
           ↓
    Combine Logs
           ↓
  Brute Force Detector
           ↓
brute_force_alerts.csv
           ↓
    Dashboard Visualization
```

## Technical Details

### Apache Log Format
```
10.0.0.5 - - [04/Dec/2025:00:47:10 -0700] "GET /index.html HTTP/1.1" 401 1256 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
```

Parsed fields: `ip`, `timestamp`, `method`, `url`, `protocol`, `status`, `size`, `referrer`, `user_agent`

### SSH Log Format
```
2025-12-04 00:27:54 server1 sshd[1234]: Failed password for invalid user admin from 172.16.0.8 port 46429 ssh2
2025-12-04 00:54:26 server1 sshd[1234]: Accepted password for test from 192.168.1.20 port 53684 ssh2
```

Parsed fields: `timestamp`, `action`, `user`, `ip`, `port`

### Detection Algorithm

1. **Filter** failed attempts: Apache 401s + SSH "Failed password" entries
2. **Group** by IP address
3. **Resample** to 1-minute windows
4. **Alert** when count ≥ threshold (default: 5)
5. **Aggregate** sources when multiple services are attacked simultaneously

## Example Scenarios

### Scenario 1: SSH Brute Force
Attacker from IP `10.0.0.5` attempts rapid SSH password guessing:
```
Alert: 43 failed SSH attempts in 1 minute window
→ Likely brute-force attack detected
```

### Scenario 2: Web Application Attack
Same attacker targets web server with repeated 401 (Unauthorized) responses:
```
Alert: 22 failed Apache 401s in 1 minute window
→ Brute-force attack on web interface
```

### Scenario 3: Multi-Service Attack
Coordinated attack detected across both services:
```
Alerts: 
  - ssh: 11 attempts (00:21)
  - apache: 10 attempts (07:21)
→ Same IP attacking multiple services
```

## Limitations & Future Enhancements

### Current Limitations
- Fixed 1-minute detection window (configurable but not dynamic)
- Single threshold for all attack types
- No persistent alerting/notification system
- No historical data correlation

### Potential Improvements
- [ ] Machine learning-based anomaly detection
- [ ] Integration with threat intelligence feeds (IP reputation)
- [ ] Email/Slack alerting system
- [ ] Automated response (IP blocking, rate limiting)
- [ ] Dashboard persistence and historical analysis
- [ ] Support for additional log sources (Nginx, FTP, Database logs)
- [ ] User authentication and role-based access
- [ ] Attack pattern correlation and campaign detection

## Troubleshooting

### No alerts detected
- Check that log files exist in `data/` directory
- Verify threshold setting (default is 5 attempts per minute)
- Ensure timestamp parsing is correct (check `parsed_*.csv` files)

### Dashboard won't load
- Ensure Dash is installed: `pip install dash`
- Check port 8050 is available
- Review Flask debug output for errors

### Parser errors
- Verify log format matches expected regex patterns
- Check timezone consistency (mixed timezones may cause issues)
- Review parser output for "NO MATCH" warnings

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Areas for enhancement:
- Additional log source parsers
- Improved detection algorithms
- Dashboard UX improvements
- Documentation and examples

## Support

For issues or questions, open an issue or contact the project maintainer.
