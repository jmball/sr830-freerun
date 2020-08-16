"""Setup and monitor SRS SR830 freerun."""
import collections

import dash
import dash_core_components as dcc
import dash_html_components as html
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
    font={"size": 16}, margin=dict(l=20, r=0, t=30, b=0), plot_bgcolor="rgba(0,0,0,0)"
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
    font={"size": 16}, margin=dict(l=20, r=0, t=30, b=0), plot_bgcolor="rgba(0,0,0,0)"
)


# thread safe store for save path
save_path = collections.deque(maxlen=1)


app = dash.Dash(__name__)

app.layout = html.Div(
    html.Div(
        [
            html.Div(
                dcc.Graph(
                    id="R_graph",
                    figure=fig_R,
                    style={"width": "95vw", "height": "95vh"},
                )
            ),
            html.Div(
                dcc.Graph(
                    id="phase_graph",
                    figure=fig_phase,
                    style={"width": "95vw", "height": "95vh"},
                )
            ),
            dcc.Interval(id="interval-component", interval=1 * 2000, n_intervals=0,),
        ],
    ),
)


@app.callback(
    [
        dash.dependencies.Output("R_graph", "figure"),
        dash.dependencies.Output("phase_graph", "figure"),
    ],
    [dash.dependencies.Input("interval-component", "n_intervals")],
    [
        dash.dependencies.State("R_graph", "figure"),
        dash.dependencies.State("phase_graph", "figure"),
    ],
)
def update_graph_live(n, R_graph, phase_graph):
    """Update graph."""
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


@app.callback(inputs=[dash.dependencies.Input("start", "value")],)
def start():
    pass


@app.callback(inputs=[dash.dependencies.Input("stop", "value")],)
def stop():
    pass


@app.callback(
    dash.dependencies.Output("start", "disabled"),
    [dash.dependencies.Input("stop", "value")],
)
def set_start_enabled_state(enabled):
    return enabled


@app.callback(
    dash.dependencies.Output("stop", "disabled"),
    [dash.dependencies.Input("start", "value")],
)
def set_stop_enabled_state(enabled):
    return enabled


if __name__ == "__main__":
    # start dash server
    app.run_server(host="127.0.0.1", port=8050, debug=False)
