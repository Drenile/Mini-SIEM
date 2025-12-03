import pandas as pd
import plotly.express as px

def plot_failed_logins(alerts_df):
    if alerts_df.empty:
        print("⚠️ No alerts to plot.")
        return

    fig = px.bar(
        alerts_df,
        x="time",
        y="failed_attempts",
        color="ip",
        title="Brute-Force Login Attempts Over Time"
    )
    fig.show()

if __name__ == "__main__":
    alerts = pd.read_csv("data/brute_force_alerts.csv")
    plot_failed_logins(alerts)
