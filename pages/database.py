from dash import html, dash_table, dcc
from db_utils import *



#class to make tables all look the same
class DashTable:
    def __init__(self, df, table_id, position="fixed", top="75px", right="20px", width="675px", height="500px"):
        self.df = df
        self.table_id = table_id
        self.columns = [{"name": i, "id": i, "editable": True} for i in df.columns]
        self.data = df.to_dict("records")
        self.position = position
        self.top = top
        self.right = right
        self.width = width
        self.height = height

    def create_table(self):
        return dash_table.DataTable(
            id=self.table_id,
            columns=self.columns,
            data=self.data,
            data_previous=self.data,
            row_deletable=True,
            style_table={
                "position": self.position,
                "top": self.top,
                "right": self.right,
                "width": self.width,
                "maxHeight": self.height,
                "overflowY": "auto",
                "border": "1px solid black"
            },
            style_header={
                'backgroundColor': '#e6e6fa',
                'fontWeight': 'bold',
                'position': 'sticky',
                'top': 0,
                'Index': 2
            },
            style_cell={"textAlign": "left", "padding": "10px", "border": "1px solid black"},
            editable=True,
        )


# Actual Layout
def database_layout():
    table = DashTable(df=fetch_data("entries"),table_id="editable_table").create_table()
    table1 = DashTable(df=fetch_data("foods"),table_id="editable_table1",top="620px").create_table()
    foods_entry_form = html.Div([
        html.H3('New food'),
        html.Div([
            html.Label('Food:'),
            dcc.Input(id='food', type='text'),
            html.Label('Weight (g)'),
            dcc.Input(id='weight',type='number',style={"width":75}),
            html.Label('Fats (g):'),
            dcc.Input(id='fats', type='number', style={"width": 75}),
            html.Label('Carbs (g):'),
            dcc.Input(id='carbs', type='number',style={"width":75}),
            html.Label('Proteins (g):'),
            dcc.Input(id='proteins', type='number',style={"width":75}),
            html.Button('Add Food', id='add-food-btn', n_clicks=0),
        ], style={'display': 'flex', 'alignItems': 'center', 'gap': '5px'}),

        html.Div(id='output-message-food')
    ], style={'width':1200})

    meal_entry_form = html.Div([
        html.H3('Meal Entry'),
        html.Div([
            html.Label("Meal:"),
            dcc.Dropdown(['Snack','Breakfast','Lunch','Dinner'],'Snack',id='meal',style={'width':125}),
            html.Label('Food:'),
            dcc.Dropdown(id='food-meal', options=[{'label': i, 'value': i} for i in get_foods()], style={'width': 300}),
            html.Label('Weight (g):'),
            dcc.Input(id='weight-meal', type='number', style={"width": 75}),
            html.Button('Add Meal', id='add-meal-btn', n_clicks=0),
        ], style={'display': 'flex', 'alignItems': 'center', 'gap': '5px'}),
        html.Div(id='output-message-entry')
    ], style={'position': 'relative', 'top': 10,'width':1200})

    return html.Div([
        html.H3("Database Contents", style={"textAlign": "center"}),
        table,
        table1,
        foods_entry_form,
        meal_entry_form
    ], style={"position": "relative", "height": "90vh"})
