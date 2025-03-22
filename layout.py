from dash import html
import dash_bootstrap_components as dbc

# Sidebar layout
sidebar = html.Div(
    [
        html.H2("Macro Tracker", className="display-4"),
        html.Hr(),
        html.Img(src="https://cdn-icons-png.flaticon.com/512/25/25694.png", height=50),
        dbc.Nav(
            [
                dbc.NavLink("Database View", href="/database", active="exact", className="custom-nav-link"),
                dbc.NavLink("Settings", href="/settings", active="exact", className="custom-nav-link"),
                dbc.NavLink("Dash", href="/dashboard", active="exact", className="custom-nav-link"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style={
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "250px",
        "padding": "20px",
        "background-color": "#E6E6FA",
    },
)

# Content area
content = html.Div(id="page-content", style={"margin-left": "270px", "padding": "20px"})

