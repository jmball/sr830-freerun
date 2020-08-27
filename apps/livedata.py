"""Page for plotting live data."""

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
import numpy as np
import plotly
import plotly.subplots
import plotly.graph_objs as go

from app import app


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


layout = [
    dbc.Row(dbc.Col(dcc.Graph(id="R_graph", figure=fig_R, style={"height": "44vh"}))),
    dbc.Row(
        dbc.Col(
            dcc.Graph(id="phase_graph", figure=fig_phase, style={"height": "44vh"},)
        )
    ),
]


@app.callback(
    [
        dash.dependencies.Output("R_graph", "figure"),
        dash.dependencies.Output("phase_graph", "figure"),
    ],
    [dash.dependencies.Input("interval-component", "n_intervals")],
    [
        dash.dependencies.State("R_graph", "figure"),
        dash.dependencies.State("phase_graph", "figure"),
        dash.dependencies.State("save_path", "children"),
    ],
)
def update_graph_live(n, R_graph, phase_graph, save_path):
    """Update graph."""
    # print(session_data)
    if len(save_path) != 0:
        # # load data from save file
        # data = np.genfromtxt(
        #     save_path[0], delimiter="\t", skip_header=1, usecols=[0, 7, 8]
        # )
        # # calc experiment time from timestamp
        # data[:, 0] = data[:, 0] - data[0, 0]

        # # update graphs
        # R_graph = format_figure(data[:, [0, 1]], R_graph)
        # phase_graph = format_figure(data[:, [0, 2]], phase_graph)
        pass

    return [R_graph, phase_graph]
