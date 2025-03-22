import dash
from dash import Input, Output, State, ctx
from dash.exceptions import PreventUpdate
from db_utils import update_database

def register_callbacks(app):
    # Callback for modifying the main entries table
    @app.callback(
        Output("editable-table", "data"),
        [Input("editable-table", "data")],
        prevent_initial_call=True
    )
    def modify_entries_table(rows):
        # Check if the callback was triggered
        if not ctx.triggered:
            print("Callback triggered by an unknown event")
            raise PreventUpdate

        # Debugging: Print out the current rows to see if the callback gets triggered
        print("Callback triggered for 'editable-table'")
        print(f"Current rows: {rows}")

        # Ensure rows data is properly passed
        if rows:
            update_database(rows, "entries")
            return rows
        else:
            print("No data to update")
            raise PreventUpdate

    # Callback for modifying the food database table
    @app.callback(
        Output("editable-table1", "data"),
        [Input("editable-table1", "data")],
        prevent_initial_call=True
    )
    def modify_food_table(rows):
        # Check if the callback was triggered
        if not ctx.triggered:
            print("Callback triggered by an unknown event")
            raise PreventUpdate

        # Debugging: Print out the current rows to see if the callback gets triggered
        print("Callback triggered for 'editable-table1'")
        print(f"Current rows: {rows}")

        # Ensure rows data is properly passed
        if rows:
            update_database(rows, "foods")
            return rows
        else:
            print("No data to update")
            raise PreventUpdate
