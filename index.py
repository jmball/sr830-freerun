"""Setup and monitor SRS SR830 freerun."""
import collections

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
import numpy as np
import plotly
import plotly.subplots
import plotly.graph_objs as go


def format_figure(data, fig):
    """Format figure.

    Parameters
    ----------
    data : array
        Array of data.
    fig : dict
        Dictionary representation of Plotly figure.

    Returns
    -------
    fig : dict
        Dictionary representation of Plotly figure.
    """
    # add data to fig
    fig["data"][0]["x"] = data[:, 0]
    fig["data"][0]["y"] = data[:, 1]

    # update ranges
    fig["layout"]["xaxis"]["range"] = [min(data[:, 0]), max(data[:, 0])]
    fig["layout"]["yaxis"]["range"] = [min(data[:, 1]), max(data[:, 1])]

    return fig


fig_R = plotly.subplots.make_subplots()
fig_R.add_trace(go.Scatter(x=[], y=[], mode="lines+markers", name="R"))
fig_R.update_xaxes(
    title="time (s)",
    ticks="inside",
    mirror="ticks",
    linecolor="#444",
    showline=True,
    zeroline=False,
    showgrid=False,
    autorange=False,
)
fig_R.update_yaxes(
    title="R (V)",
    ticks="inside",
    mirror=True,
    linecolor="#444",
    showline=True,
    zeroline=False,
    showgrid=False,
    autorange=False,
)
fig_R.update_layout(
    font={"size": 16}, margin=dict(l=30, r=30, t=30, b=30), plot_bgcolor="rgba(0,0,0,0)"
)

fig_phase = plotly.subplots.make_subplots()
fig_phase.add_trace(go.Scatter(x=[], y=[], mode="lines+markers", name="Phase"))
fig_phase.update_xaxes(
    title="time (s)",
    ticks="inside",
    mirror="ticks",
    linecolor="#444",
    showline=True,
    zeroline=False,
    showgrid=False,
    autorange=False,
)
fig_phase.update_yaxes(
    title="Phase (degrees)",
    ticks="inside",
    mirror=True,
    linecolor="#444",
    showline=True,
    zeroline=False,
    showgrid=False,
    autorange=False,
)
fig_phase.update_layout(
    font={"size": 16}, margin=dict(l=30, r=30, t=30, b=30), plot_bgcolor="rgba(0,0,0,0)"
)


# thread safe store for save path
save_path = collections.deque(maxlen=1)

# style={"width": "100%", "height": "100%"},

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

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
    "margin-left": "27rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H1("SR830 Free-run", className="display-4"),
        html.Hr(),
        # html.P("A simple sidebar layout with navigation links", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink(
                    "Setup", href="setup", id="setup", style={"font-size": "20pt"},
                ),
                dbc.NavLink(
                    "Live Data",
                    href="livedata",
                    id="livedata",
                    style={"font-size": "20pt"},
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = dbc.Container([dcc.Location(id="url", refresh=False), sidebar, content],)


save_folder_input = dbc.FormGroup(
    [
        dbc.Label("Save folder"),
        dbc.Input(id="save-input", type="path", value=""),
        dbc.FormFeedback("", valid=True),
        dbc.FormFeedback(
            "Folder doesn't exist. Please choose an existing folder", valid=False,
        ),
        dbc.Tooltip(
            "Parent folder containing data files",
            target="save-input",
            placement="bottom",
        ),
    ]
)

device_id_input = dbc.FormGroup(
    [
        dbc.Label("Device ID"),
        dbc.Input(id="device-id", type="text", value=""),
        dbc.FormFeedback("", valid=True),
        dbc.FormFeedback(
            (
                "Use alphanumeric, _, and - characters only. Avoid special characters: "
                + "@, #, ~, >, <, /, etc."
            ),
            valid=False,
        ),
        dbc.Tooltip(
            "Device identifier used in data filename",
            target="device-id",
            placement="bottom",
        ),
    ]
)

interval_input = dbc.FormGroup(
    [
        dbc.Label("Measurement interval (s)"),
        dbc.Input(id="meas-interval", type="number", value=1.000, min=0),
        dbc.FormFeedback("", valid=True),
        dbc.FormFeedback("Intervals must be greater than zero", valid=False),
        dbc.Tooltip(
            "Interval between measurements in seconds",
            target="meas-interval",
            placement="bottom",
        ),
    ]
)

setup_page_content = None
livedata_page_content = None

# dcc.Interval(id="interval-component", interval=1 * 2000, n_intervals=0,),


@app.callback(
    [
        dash.dependencies.Output("R_graph", "figure"),
        dash.dependencies.Output("phase_graph", "figure"),
    ],
    [
        dash.dependencies.Input("interval-component", "n_intervals"),
        dash.dependencies.Input("url", "pathname"),
    ],
    [
        dash.dependencies.State("R_graph", "figure"),
        dash.dependencies.State("phase_graph", "figure"),
    ],
)
def update_graph_live(n, pathname, R_graph, phase_graph):
    """Update graph."""
    if pathname == "/livedata":
        if len(save_path) != 0:
            # load data from save file
            data = np.genfromtxt(
                save_path[0], delimiter="\t", skip_header=1, usecols=[0, 7, 8]
            )
            # calc experiment time from timestamp
            data[:, 0] = data[:, 0] - data[0, 0]

            # update graphs
            R_graph = format_figure(data[:, [0, 1]], R_graph)
            phase_graph = format_figure(data[:, [0, 2]], phase_graph)

        return [R_graph, phase_graph]


# @app.callback(
#     dash.dependencies.Output("tab-content", "children"),
#     [dash.dependencies.Input("tabs", "active_tab")],
# )
# def render_page(active_tab):
#     """Render content for the active tab."""
#     if active_tab is not None:
#         if active_tab == "setup":
#             return dbc.Container()
#         elif active_tab == "view":
#             return dbc.Container(
#                 [
#                     dbc.Row(
#                         dbc.Col(dcc.Graph(id="R_graph", figure=fig_R,), width=12,),
#                         justify="center",
#                     ),
#                     dbc.Row(
#                         dbc.Col(
#                             dcc.Graph(id="phase_graph", figure=fig_phase), width=12
#                         ),
#                         justify="center",
#                     ),
#                 ]
#             )
#     return "No tab selected"

# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    [
        dash.dependencies.Output("setup", "active"),
        dash.dependencies.Output("livedata", "active"),
    ],
    [dash.dependencies.Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if (pathname == "/") or (pathname == "/setup"):
        # Treat page 1 as the homepage / index
        return True, False
    else:
        return False, True


@app.callback(
    dash.dependencies.Output("page-content", "children"),
    [dash.dependencies.Input("url", "pathname")],
)
def render_page_content(pathname):
    if pathname == "/setup":
        return [save_folder_input, device_id_input, interval_input]
    elif pathname == "/livedata":
        return html.P("This is the content of page 2. Yay!")
    else:
        # If the user tries to reach a different page, return a 404 message
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised."),
            ]
        )


if __name__ == "__main__":
    # start dash server
    app.run_server(host="127.0.0.1", port=8050, debug=True)
