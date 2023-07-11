import dash
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages=True, )

navbar = dbc.NavbarSimple(
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(page["name"], href=page["path"])
            for page in dash.page_registry.values()
            if page["module"] != "pages.not_found_404"
        ],
        nav=True,
        label="",
    ),
   # brand="Digital Methane Tracking",
    color='#1f2c56',
    dark=True,
    className="mb-2",
)

app.layout = dbc.Container(
    [navbar, dash.page_container],
    fluid=True,
)

if __name__ == "__main__":
    app.run_server(debug=True)