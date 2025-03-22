from dash import html, dcc

from db_utils import fetch_data


def settings_layout():
    return html.Div([
        html.H3("Settings", style={"textAlign": "center"}),
        dcc.Input(id="username", type="text", placeholder="Enter Username"),
        dcc.Dropdown(
            id="theme-dropdown",
            options=[
                {"label": "Light", "value": "light"},
                {"label": "Dark", "value": "dark"}
            ],
            placeholder="Select Theme"
        )
    ])
