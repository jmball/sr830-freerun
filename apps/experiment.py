"""Setup page.

N.B. dbc.Select component values are 1-indexed becuase they derive from the HTML
<select> element (https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select).
Value mappings for the lock-in amplifier are 0-indexed so values read from Select
components must be decremented before being sent to the lock-in amplifier.
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from app import app


save_folder_input = dbc.FormGroup(
    [
        dbc.Label("Save folder"),
        dbc.Input(
            id="save-input",
            type="path",
            value="",
            persistence=True,
            persistence_type="session",
        ),
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
        dbc.Input(
            id="device-id",
            type="text",
            value="",
            persistence=True,
            persistence_type="session",
        ),
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
        dbc.Input(
            id="meas-interval",
            type="number",
            value=1.000,
            min=0,
            persistence=True,
            persistence_type="session",
        ),
        dbc.FormFeedback("", valid=True),
        dbc.FormFeedback("Intervals must be greater than zero", valid=False),
        dbc.Tooltip(
            "Interval between measurements in seconds",
            target="meas-interval",
            placement="bottom",
        ),
    ]
)

timeout_input = dbc.FormGroup(
    [
        dbc.Label("Timeout (s)"),
        dbc.Input(
            id="timeout",
            type="number",
            value=-1,
            min=-1,
            persistence=True,
            persistence_type="session",
        ),
        dbc.FormFeedback("", valid=True),
        dbc.FormFeedback("Timeout must be greater than or equal to -1", valid=False),
        dbc.Tooltip(
            "Total experiment time. Set to -1 to run until stop is pressed.",
            target="timeout",
            placement="bottom",
        ),
    ]
)

layout = html.Div(
    [
        dbc.Row(
            [dbc.Col(save_folder_input, width=6), dbc.Col(device_id_input, width=6)],
            form=True,
        ),
        dbc.Row(
            [dbc.Col(interval_input, width=6), dbc.Col(timeout_input, width=6)],
            form=True,
        ),
    ]
)
