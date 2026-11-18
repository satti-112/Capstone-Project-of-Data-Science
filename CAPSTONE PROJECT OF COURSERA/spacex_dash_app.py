# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()
sites = sorted(spacex_df["Launch Site"].unique())

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1("SpaceX Launch Records Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 40}),

    # TASK 1: Launch-site dropdown
    dcc.Dropdown(id="site-dropdown",
                 options=[{"label": "All Sites", "value": "ALL"}] + [{"label": s, "value": s} for s in sites],
                 value="ALL",
                 placeholder="Select a Launch Site here",
                 searchable=True),
    html.Br(),

    # TASK 2: Success pie chart
    html.Div(dcc.Graph(id="success-pie-chart")),
    html.Br(),

    html.P("Payload range (Kg):"),
    # TASK 3: Payload range slider
    dcc.RangeSlider(id="payload-slider", min=0, max=10000, step=1000,
                    marks={i: str(i) for i in range(0, 10001, 2500)},
                    value=[min_payload, max_payload]),

    # TASK 4: Payload vs. outcome scatter chart
    html.Div(dcc.Graph(id="success-payload-scatter-chart")),
])

# TASK 2 callback
@app.callback(Output("success-pie-chart", "figure"),
              Input("site-dropdown", "value"))
def get_pie_chart(entered_site):
    if entered_site == "ALL":
        fig = px.pie(spacex_df, values="class", names="Launch Site",
                     title="Total Success Launches By Site")
    else:
        site_df = spacex_df[spacex_df["Launch Site"] == entered_site]
        counts = site_df["class"].value_counts().reset_index()
        counts.columns = ["class", "count"]
        fig = px.pie(counts, values="count", names="class",
                     title=f"Total Success Launches for site {entered_site}")
    return fig

# TASK 4 callback
@app.callback(Output("success-payload-scatter-chart", "figure"),
              [Input("site-dropdown", "value"), Input("payload-slider", "value")])
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    df = spacex_df[(spacex_df["Payload Mass (kg)"] >= low) & (spacex_df["Payload Mass (kg)"] <= high)]
    if entered_site == "ALL":
        title = "Correlation between Payload and Success for all Sites"
    else:
        df = df[df["Launch Site"] == entered_site]
        title = f"Correlation between Payload and Success for site {entered_site}"
    return px.scatter(df, x="Payload Mass (kg)", y="class", color="Booster Version Category", title=title)

if __name__ == "__main__":
    app.run(debug=False, port=8050)