# plot_alerts.py
import pandas as pd
import plotly.express as px

def plot_failed_logins(alerts_csv="data/brute_force_alerts.csv"):
    try:
        alerts = pd.read_csv(alerts_csv)
    except Exception as e:
        print("Could not load alerts:", e)
        return

    if alerts.empty:
        print("No alerts to plot.")
        return

    alerts['time'] = pd.to_datetime(alerts['time'], errors='coerce')
    fig = px.bar(alerts, x='time', y='failed_attempts', color='source', hover_data=['ip'])
    fig.show()

if __name__ == "__main__":
    plot_failed_logins()

