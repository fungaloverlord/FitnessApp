from dash import html, dcc

def dashboard_layout():
    return html.Div([
        html.H3("Dashboard Overview", style={"textAlign": "center"}),
        dcc.Graph(id="macro-chart"),
    ])
