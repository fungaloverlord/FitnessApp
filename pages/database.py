from dash import html, dash_table, dcc
from db_utils import *

#class to make tables all look the same
class DashTable:
    def __init__(self, df, table_id, position="relative", top="0px", right="0px", width="675px", height="500px" ):
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
    table1 = DashTable(df=fetch_data("foods"),table_id="editable_table1").create_table()

    # entry forms
    foods_entry_form = html.Div([
        html.H3('New Food'),
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
    ], style={'position': 'relative', 'top': '10px','width':'1200px'})

    # Tab setup
    tabs = html.Div([
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Daily', value='tab-1'),
        dcc.Tab(label='Weekly', value='tab-2'),
    ]),
    html.Div(id='tabs-content')
    ],style={'position': 'relative','top': '50px','width': '1200px'})

    return (
        html.Div(
            className="responsive-row",  # Apply the responsive-row class for the parent div
            children=[
                # First Column
                html.Div(
                    className="responsive-column",  # Apply the responsive-column class for the first column
                    children=[
                        html.H3("Database Contents", style={"textAlign": "center"}),
                        foods_entry_form,
                        meal_entry_form,
                        tabs
                    ]
                ),
                # Second Column
                html.Div(
                    className="responsive-column",  # Apply the responsive-column class for the second column
                    children=[
                        html.H3("Tables"),
                        html.H5("Entries", style={"padding": 10}),
                        table,
                        html.H5("Foods", style={"padding": 10}),
                        table1,
                    ]
                )
            ]
        )
    )

def tab1_layout():

    return html.Div([

    ], style={"position": "relative", "height": "90vh"})