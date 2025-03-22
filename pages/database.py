from dash import html, dash_table
from db_utils import *



#class to make tables all look the same
class DashTable:
    def __init__(self, df, table_id, position="fixed", top="75px", right="20px", width="650px", height="700px"):
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
                'zIndex': 2
            },
            style_cell={"textAlign": "left", "padding": "10px", "border": "1px solid black"},
            editable=True
        )

# Actual Layout
def database_layout():

    table = DashTable(df=fetch_data("entries"),table_id="editable_table", height="300px").create_table()
    table1 = DashTable(df=fetch_data("foods"),table_id="editable_table1",top="650px").create_table()

    return html.Div([
        html.H3("Database Contents", style={"textAlign": "center"}),
        table,
        table1
    ], style={"position": "relative", "height": "90vh"})
