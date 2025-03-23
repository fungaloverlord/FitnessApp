from dash import Input, Output, State, html
from db_utils import update_database, fetch_data, add_new_food,add_new_entry

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
            if not all([food, weight, carbs, proteins, fats]):
                return html.Em('Please fill in all fields.', style={'position': 'fixed', 'top': 71, 'left': 420,'color': 'red'})

            try:
                # Ensure that weight, carbs, proteins, and fats are converted to numbers
                weight = float(weight)
                carbs = float(carbs)
                proteins = float(proteins)
                fats = float(fats)
                # Call the function to add the new food
                add_new_food(food, weight, fats, carbs, proteins)

                return html.Em('Meal added successfully!', style={'position': 'fixed', 'top': 71, 'left': 420,'color': 'green'})

            except ValueError:
                return html.Em('Please enter valid numerical values for weight, carbs, proteins, and fats.',
                               style={'position': 'fixed', 'top': 71, 'left': 420,'color': 'red'})

            except Exception as e:
                return html.Em(f'Error adding meal: {e}', style={'position': 'fixed', 'top': 71, 'left': 420,'color': 'red'})

        return html.Em('Ready', style={'position': 'fixed', 'top': 71, 'left': 420,'color': 'purple'})

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
                return html.Em('Please fill in all fields.', style={'position': 'fixed','top':155,'left':430,'color': 'red'})

            try:
                # Convert inputs to float where applicable
                add_new_entry(meal=meal, food=food, weight=float(weight))

                return html.Em('Meal added successfully!', style={'position': 'fixed','top':155,'left':430,'color': 'green'})

            except ValueError:
                return html.Em('Please enter valid numerical values for weight.', style={'position': 'fixed','top':155,'left':430,'color': 'red'})

            except Exception as e:
                return html.Em(f'Error adding meal: {e}', style={'position': 'fixed','top':155,'left':430,'color': 'red'})

        return html.Em('Ready', style={'position': 'fixed','top':155,'left':430,'color': 'purple'})






