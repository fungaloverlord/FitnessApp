from dash import Input, Output, State, html, dcc
from db_utils import update_database, add_new_food, add_new_entry, create_gauge_figure, create_macro_figure, daily_macros


def register_callbacks(app):
    # Callback for modifying the main entries table and foods table
    @app.callback(
        Output("editable_table", "data"),
        Input("editable_table", "data"),
        prevent_initial_call=True
    )
    def modify_entries_table(rows):
        try:
            update_database(rows, "entries")
            return rows
        except Exception as e:
            print(f"Error updating entries: {e}")
            raise

    @app.callback(
        Output("editable_table1", "data"),
        Input("editable_table1", "data"),
        prevent_initial_call=True
    )
    def modify_food_table(rows):
        try:
            update_database(rows, "foods")
            return rows
        except Exception as e:
            print(f"Error updating foods: {e}")
            raise

    @app.callback(
        Output('output-message-food', 'children'),
        Input('add-food-btn', 'n_clicks'),
        [State('food', 'value'),
         State('weight', 'value'),
         State('fats', 'value'),
         State('carbs', 'value'),
         State('proteins', 'value')]
    )

    def add_food(n_clicks, food, weight, fats, carbs, proteins):
        if n_clicks > 0:
            # Check if all fields have values
            if not all(i is not None for i in [food, weight, carbs, proteins, fats]):
                return html.Em('Please fill in all fields.', style={'position': 'relative', 'top': 80, 'left': 450,'color': 'red'})

            try:
                # Ensure that weight, carbs, proteins, and fats are converted to numbers
                weight = float(weight)
                carbs = float(carbs)
                proteins = float(proteins)
                fats = float(fats)
                # Call the function to add the new food
                add_new_food(food, weight, fats, carbs, proteins)

                return html.Em('Meal added successfully!', style={'position': 'fixed', 'top': 80, 'left': 450,'color': 'green'})

            except ValueError:
                return html.Em('Please enter valid numerical values for weight, carbs, proteins, and fats.',
                               style={'position': 'fixed', 'top': 80, 'left': 450,'color': 'red'})

            except Exception as e:
                return html.Em(f'Error adding meal: {e}', style={'position': 'fixed', 'top': 80, 'left': 450,'color': 'red'})

        return html.Em('Ready', style={'position': 'fixed', 'top': 80, 'left': 450,'color': 'purple'})

    @app.callback(
        Output('output-message-entry', 'children'),
        Input('add-meal-btn', 'n_clicks'),
        [State('meal', 'value'),
         State('food-meal', 'value'),
         State('weight-meal', 'value')]
    )
    def add_new_entry_callback(n_clicks, meal, food, weight):
        if n_clicks > 0:
            # Check if all fields have values
            if not all([meal, food, weight]):
                return html.Em('Please fill in all fields.', style={'position': 'fixed','top':165,'left':450,'color': 'red'})

            try:
                # Convert inputs to float where applicable
                add_new_entry(meal=meal, food=food, weight=float(weight))

                return html.Em('Meal added successfully!', style={'position': 'fixed','top':165,'left':450,'color': 'green'})

            except ValueError:
                return html.Em('Please enter valid numerical values for weight.', style={'position': 'fixed','top':165,'left':450,'color': 'red'})

            except Exception as e:
                return html.Em(f'Error adding meal: {e}', style={'position': 'fixed','top':165,'left':450,'color': 'red'})

        return html.Em('Ready', style={'position': 'fixed','top':165,'left':450,'color': 'purple'})

    @app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))

    def render_content(tab):
        target_calories = 2200
        consumed_calories = sum(daily_macros().total)
        remaining_calories = target_calories - consumed_calories

        protein_target = 175
        fat_target = target_calories * .2 / 9

        carbs_target = target_calories * .48 / 4
        print(carbs_target)
        if tab == 'tab-1':
            drop = 500
            bar_drop = drop + 180
            label_drop = bar_drop + 115
            return html.Div([
                html.H3('Daily Nutrition'),
                    html.Div([
                        dcc.Graph(figure=create_macro_figure(sum(daily_macros().protein), protein_target, 'Protein', '#f28500'),
                                  config={"displayModeBar": False, "scrollZoom": False, "doubleClick": "reset",},
                                  style={"position": 'fixed', 'width': 300, 'top': bar_drop, 'left': 535}),
                        html.Label('Protein', style={"position": 'fixed', 'width': 300, 'top': label_drop, 'left': 655}),
                        dcc.Graph(figure=create_macro_figure(sum(daily_macros().fat), fat_target, 'Fat', '#ffcc00'),
                                  config={"displayModeBar": False, "scrollZoom": False, "doubleClick": "reset", },
                                  style={"position": 'fixed', 'width': 300, 'top': bar_drop, 'left': 750}),
                        html.Label('Fat', style={"position": 'fixed', 'width': 300, 'top': label_drop, 'left': 880}),
                        dcc.Graph(figure=create_macro_figure(sum(daily_macros().carb), carbs_target, 'Carbs', '#00cc66'),
                                  config={"displayModeBar": False, "scrollZoom": False, "doubleClick": "reset", },
                                  style={"position": 'fixed', 'width': 300, 'top': bar_drop, 'left': 965}),
                        html.Label('Carb', style={"position": 'fixed', 'width': 300, 'top': label_drop, 'left': 1095}),
                    ], style={'display': 'flex'}),
                    dcc.Graph(figure=create_gauge_figure(),
                              config={"displayModeBar": False, "scrollZoom": False, "doubleClick": "reset", },
                              style={"position": 'fixed', 'top': drop, 'left': 700, 'width': 400}),
                ])
        elif tab == 'tab-2':
            return html.Div([
                html.H3('Tab content 2')
            ])





