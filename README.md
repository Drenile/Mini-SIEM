# Mini-SIEM Project

This project simulates a mini-SIEM system that parses logs, detects brute-force login attempts, and visualizes alerts.

## Features
- Apache log parsing
- Brute force detection
- Interactive dashboard

## How to Run
1. Place your logs in `data/`
2. Run `parser/apache_parser.py` to parse logs
3. Run `detection/brute_force_detector.py` to detect suspicious IPs
4. Run `dashboard/plot_alerts.py` to visualize alerts

## Sample Output
![screenshot](screenshot.png)

## Future Improvements
- Add support for SSH logs
- Integrate threat intelligence feeds
- Build alerting system
