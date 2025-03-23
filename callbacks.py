from dash import Input, Output, State, ctx
from dash.exceptions import PreventUpdate
from db_utils import update_database, fetch_data, add_new_food
import pandas as pd

def register_callbacks(app):
    # Callback for modifying the main entries table and foods table
    @app.callback(
        Output("editable_table", "data"),
        Input("editable_table", "data"),
        prevent_initial_call=True
    )
    def modify_entries_table(rows):
        try:
            print(rows)
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
            print(type(rows))
            update_database(rows, "foods")
            return rows
        except Exception as e:
            print(f"Error updating foods: {e}")
            raise

    @app.callback(
        Output('output-message', 'children'),
        Input('add-meal-btn', 'n_clicks'),
        [State('food', 'value'),
         State('weight', 'value'),
         State('fats', 'value'),
         State('carbs', 'value'),
         State('proteins', 'value')]
    )
    def add_meal(n_clicks, food, weight, carbs, proteins, fats):
        if n_clicks > 0:
            # Check if all fields have values
            if not all([food, weight, carbs, proteins, fats]):
                return 'Please fill in all fields.'

            try:
                # Convert inputs to float where applicable
                new_food = food
                weight = float(weight)
                carbs = float(carbs)
                proteins = float(proteins)
                fats = float(fats)

                # get next id
                food_data = fetch_data('foods')
                if 'id' in food_data.columns:
                    new_id = str(max([int(x) for x in fetch_data('foods')['id']]) + 1)
                else:
                    new_id = '1'  # Start from 1 if 'id' column is not found

                print(f"Next ID: {new_id}")

                add_new_food(new_id,new_food,weight,fats,carbs,proteins)

                return 'Meal added successfully!'

            except ValueError:
                return 'Please enter valid numerical values for weight, carbs, proteins, and fats.'

            except Exception as e:
                return f'Error adding meal: {e}'

        return 'Please fill in all fields.'





