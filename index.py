"""Setup and monitor SRS SR830 freerun."""

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from app import app
from apps import settings, livedata

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "25rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "23rem",
    "margin-right": "2rem",
    "padding": "1rem 1rem",
}

sidebar = html.Div(
    [
        html.H1("SR830 Free-run", className="display-4"),
        html.Hr(),
        # html.P("A simple sidebar layout with navigation links", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink(
                    "Setup", href="setup", id="setup", style={"font-size": "18pt"},
                ),
                dbc.NavLink(
                    "Live Data",
                    href="livedata",
                    id="livedata",
                    style={"font-size": "18pt"},
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

button_bar = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button("Start", id="start", color="success", block=True),
                    width=4,
                ),
                dbc.Col(
                    dbc.Button(
                        "Stop", id="stop", color="danger", block=True, disabled=True
                    ),
                    width=4,
                ),
                dbc.Col(
                    dbc.Button("Exit", id="exit", color="primary", block=True), width=4
                ),
            ]
        ),
        html.Hr(),
    ],
    style=CONTENT_STYLE,
)

page_content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = dbc.Container(
    [
        dcc.Location(id="url", refresh=False),
        # dcc.Store(id="session", data={"save_folder": ""}, storage_type="memory"),
        html.Div(id="save_path", children="", hidden=True),
        dcc.Interval(id="interval-component", interval=1 * 2000, n_intervals=0,),
        sidebar,
        button_bar,
        page_content,
    ],
)


@app.callback(
    dash.dependencies.Output("page-content", "children"),
    [dash.dependencies.Input("url", "pathname")],
    [dash.dependencies.State("save_path", "children")],
)
def display_page(pathname, save_path):
    """Display selected page."""
    if pathname in ["/", "/setup"]:
        return settings.layout
    elif pathname == "/livedata":
        return livedata.layout
    else:
        # If the user tries to reach a different page, return a 404 message
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised."),
            ]
        )


@app.callback(
    [
        dash.dependencies.Output("setup", "active"),
        dash.dependencies.Output("livedata", "active"),
    ],
    [dash.dependencies.Input("url", "pathname")],
)
def toggle_active_links(pathname):
    """Set the active state of navlinks."""
    if pathname in ["/", "/setup"]:
        # Treat page 1 as the homepage / index
        return True, False
    elif pathname == "/livedata":
        return False, True
    else:
        return False, False


if __name__ == "__main__":
    # start dash server
    app.run_server(host="127.0.0.1", port=8050, debug=True)
