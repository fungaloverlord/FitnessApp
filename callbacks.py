from dash import Input, Output, State, ctx
from dash.exceptions import PreventUpdate
from db_utils import update_database

def register_callbacks(app):
    # Callback for modifying the main entries table and foods table
    @app.callback(
        Output("editable_table", "data"),
        Output("editable_table1", "data"),
        Input("editable_table", "data_previous"),
        Input("editable_table", "data"),
        Input("editable_table1", "data_previous"),
        Input("editable_table1", "data"),
        prevent_initial_call=True
    )
    def modify_tables(prev_data1, rows1, prev_data2, rows2):
        if not ctx.triggered:
            raise PreventUpdate

        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
        print(f"Callback triggered by: {trigger_id}")

        # Update database only if data has changed
        if trigger_id == "editable_table" and prev_data1 != rows1:
            print("Updating entries table with new data")
            update_database(rows1, "entries")
            return rows1
        elif trigger_id == "editable_table1" and prev_data2 != rows2:
            print("Updating foods table with new data")
            update_database(rows2, "foods")
            return rows2
        else:
            print("No changes detected, skipping update")
            raise PreventUpdate