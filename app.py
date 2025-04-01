import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from layout import sidebar, content
from pages.database import database_layout
from pages.dashboard import dashboard_layout
from pages.settings import settings_layout
from callbacks import register_callbacks  # Import other callbacks

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "Macro Tracker"
server = app.server  # Required for deployment

# App layout
app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])


# Single callback for routing pages
@app.callback(
    dash.Output("page-content", "children"),
    [dash.Input("url", "pathname")]
)
def display_page(pathname):
    try:
        if pathname == "/database":
            return database_layout()
        elif pathname == "/dashboard":
            return dashboard_layout()
        elif pathname == "/settings":
            return settings_layout()
        else:
            return html.H3("Welcome to the Home Page")
    except Exception as e:
        print(f"Error rendering page: {e}")
        return html.H3("An error occurred. Please try again.")


# Register callbacks for interactivity (EXCEPT page-content updates)???
register_callbacks(app)

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=8050, debug=True)
