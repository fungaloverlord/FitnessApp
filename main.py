import dash
from dash import dcc, html, Input, Output, State, dash_table
import sqlite3
import pandas as pd
import plotly.express as px

# Initialize the app
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Layout
app.layout = html.Div([
    html.H1('Meal Macro Tracker'),
    html.Div([
        html.Label('Meal Name:'),
        dcc.Input(id='meal-name', type='text'),

        html.Label('Date:'),
        dcc.Input(id='meal-date', type='date'),

        html.Label('Meal Type:'),
        dcc.Dropdown(id='meal-type', options=[
            {'label': 'Breakfast', 'value': 'Breakfast'},
            {'label': 'Lunch', 'value': 'Lunch'},
            {'label': 'Dinner', 'value': 'Dinner'},
            {'label': 'Snack', 'value': 'Snack'}
        ]),

        html.Label('Carbs (g):'),
        dcc.Input(id='carbs', type='number'),
        html.Label('Proteins (g):'),
        dcc.Input(id='proteins', type='number'),
        html.Label('Fats (g):'),
        dcc.Input(id='fats', type='number'),
        html.Label('Calories:'),
        dcc.Input(id='calories', type='number'),

        html.Button('Add Meal', id='add-meal-btn', n_clicks=0),
    ]),

    html.Div(id='output-message'),
    html.H2('Meal Data'),
    dash_table.DataTable(id='meal-table'),

    html.H2('Stats'),
    dcc.Graph(id='macro-chart'),
])

# Callbacks to add data and show results
def get_data():
    conn = sqlite3.connect('meal_data.db')
    df = pd.read_sql_query('''SELECT Meals.date, Meals.name, Meals.meal_type, Macros.carbs, Macros.proteins, Macros.fats, Macros.calories
                                FROM Meals JOIN Macros ON Meals.meal_id = Macros.meal_id''', conn)
    conn.close()
    return df

@app.callback(
    Output('output-message', 'children'),
    Input('add-meal-btn', 'n_clicks'),
    [State('meal-name', 'value'), State('meal-date', 'value'), State('meal-type', 'value'),
     State('carbs', 'value'), State('proteins', 'value'), State('fats', 'value'), State('calories', 'value')]
)
def add_meal(n_clicks, name, date, meal_type, carbs, proteins, fats, calories):
    if n_clicks > 0 and all([name, date, meal_type, carbs, proteins, fats, calories]):
        conn = sqlite3.connect('meal_data.db')
        c = conn.cursor()
        c.execute('INSERT INTO Meals (name, date, meal_type) VALUES (?, ?, ?)', (name, date, meal_type))
        meal_id = c.lastrowid
        c.execute('INSERT INTO Macros (meal_id, carbs, proteins, fats, calories) VALUES (?, ?, ?, ?, ?)',
                  (meal_id, carbs, proteins, fats, calories))
        conn.commit()
        conn.close()
        return 'Meal added successfully!'
    return 'Please fill in all fields.'

@app.callback(
    Output('meal-table', 'data'),
    Output('macro-chart', 'figure'),
    Input('add-meal-btn', 'n_clicks')
)
def update_output(n_clicks):
    df = get_data()
    table_data = df.to_dict('records')
    fig = px.pie(df, values='calories', names='meal_type', title='Calories by Meal Type')
    return table_data, fig

if __name__ == '__main__':
    app.run_server(debug=True)


