# dashboard.py
import pandas as pd
from dash import Dash, dcc, html, Output, Input
import plotly.express as px
import plotly.graph_objects as go
from detection.brute_force_detector import detect_brute_force

def load_combined():
    logs = []
    try:
        a = pd.read_csv("data/parsed_apache.csv")
        a['source'] = a.get('source', 'apache')
        logs.append(a)
    except Exception:
        pass

    try:
        s = pd.read_csv("data/parsed_ssh.csv")
        s['source'] = s.get('source', 'ssh')
        logs.append(s)
    except Exception:
        pass

    if not logs:
        return pd.DataFrame(), pd.DataFrame()

    combined = pd.concat(logs, ignore_index=True, sort=False)
    # ensure timestamp exists and parsed
    combined['timestamp'] = pd.to_datetime(combined['timestamp'], errors='coerce')
    # run detection on combined
    alerts = detect_brute_force(combined)
    return combined, alerts

app = Dash(__name__)
app.title = "Mini-SIEM (Apache + SSH)"

app.layout = html.Div([
    html.H1("Mini-SIEM Dashboard (Apache + SSH)", style={"textAlign":"center"}),
    dcc.Interval(id="interval", interval=5000, n_intervals=0),

    html.Div([
        html.Div([
            dcc.Graph(id="req-over-time", style={"height":"400px"})
        ], style={"width":"66%", "display":"inline-block", "padding":"10px", "verticalAlign":"top"}),

        html.Div([
            dcc.Graph(id="status-dist", style={"height":"400px"}),
            dcc.Graph(id="bruteforce-chart", style={"height":"300px"})
        ], style={"width":"33%", "display":"inline-block", "padding":"10px"})
    ])
], style={"maxWidth":"1200px", "margin":"0 auto"})

@app.callback(
    Output("req-over-time", "figure"),
    Output("status-dist", "figure"),
    Output("bruteforce-chart", "figure"),
    Input("interval", "n_intervals")
)
def update(n):
    logs, alerts = load_combined()

    if logs.empty:
        empty = px.scatter(title="No logs available")
        return empty, empty, empty

    # Requests over time (binned)
    try:
        df_time = logs.copy()
        df_time = df_time.dropna(subset=['timestamp'])
        df_time['minute'] = df_time['timestamp'].dt.floor('min')
        time_counts = df_time.groupby(['minute']).size().reset_index(name='count')
        req_fig = px.line(time_counts, x='minute', y='count', title="Requests Over Time")
    except Exception as e:
        req_fig = px.scatter(title=f"Error building time series: {e}")

    # Status distribution (by source stacked)
    try:
        status_df = logs.groupby(['source','status']).size().reset_index(name='count')
        status_fig = px.bar(status_df, x='status', y='count', color='source', barmode='group',
                            title="Status Code Distribution by Source")
    except Exception as e:
        status_fig = px.scatter(title=f"Error building status distribution: {e}")

    # Brute-force alerts (combined)
    if alerts.empty:
        bf_fig = go.Figure()
        bf_fig.add_annotation(text="No brute-force alerts detected", x=0.5, y=0.5, showarrow=False)
        bf_fig.update_layout(title="Brute Force Attempts")
    else:
        # ensure time as datetime for plotting
        alerts['time'] = pd.to_datetime(alerts['time'], errors='coerce')
        bf_fig = px.bar(alerts, x='time', y='failed_attempts', color='source', hover_data=['ip'],
                        title="Brute Force Attempts (by source)")
    return req_fig, status_fig, bf_fig

if __name__ == "__main__":
    app.run(debug=True)
