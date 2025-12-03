import pandas as pd
from dash import Dash, dcc, html, Output, Input
import plotly.express as px
import plotly.graph_objects as go

from detection.brute_force_detector import detect_brute_force

# -------------------------------
# Load logs once
# -------------------------------
apache_logs = pd.read_csv("data/parsed_apache.csv")
apache_logs["timestamp"] = pd.to_datetime(apache_logs["timestamp"])

bf_alerts = detect_brute_force(apache_logs)

# -------------------------------
# App
# -------------------------------
app = Dash(__name__)

app.layout = html.Div(style={"padding": "20px"}, children=[
    html.H1("Mini SIEM Dashboard", style={"textAlign": "center"}),

    # Refresh every 5 seconds
    dcc.Interval(id="interval", interval=5000, n_intervals=0),

    html.Div([
        dcc.Graph(id="req-over-time", style={"height": "350px"}),
        dcc.Graph(id="status-dist", style={"height": "350px"}),
        dcc.Graph(id="bruteforce-chart", style={"height": "350px"}),
    ], style={
        "display": "grid",
        "gridTemplateColumns": "1fr 1fr",
        "gap": "25px"
    })
])


# -------------------------------
# CALLBACKS
# -------------------------------
@app.callback(
    Output("req-over-time", "figure"),
    Output("status-dist", "figure"),
    Output("bruteforce-chart", "figure"),
    Input("interval", "n_intervals")
)
def update_dashboard(n):

    # --- Request Volume Chart ---
    req_fig = px.histogram(
        apache_logs,
        x="timestamp",
        nbins=40,
        title="Requests Over Time"
    )

    # --- Status Code Pie ---
    status_counts = apache_logs["status"].value_counts().reset_index()
    status_counts.columns = ["status", "count"]

    status_fig = px.pie(
        status_counts,
        names="status",
        values="count",
        title="HTTP Status Distribution"
    )

    # --- Brute Force Alerts ---
    if bf_alerts.empty:
        bf_fig = go.Figure()
        bf_fig.add_annotation(
            text="No brute-force alerts detected",
            x=0.5, y=0.5,
            showarrow=False
        )
        bf_fig.update_layout(title="Brute Force Attempts")
    else:
        bf_fig = px.bar(
            bf_alerts,
            x="time",
            y="failed_attempts",
            color="ip",
            title="Brute Force Login Attempts Over Time"
        )

    return req_fig, status_fig, bf_fig


if __name__ == "__main__":
    app.run(debug=True)
