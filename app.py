"""Create dash application server."""

import dash
import dash_bootstrap_components as dbc


app = dash.Dash(
    __name__,
    eager_loading=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)
server = app.server
