"""Setup page."""
import decimal

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import sr830

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

input_config_options = []
for ix, option in enumerate(sr830.sr830().input_configurations):
    input_config_options.append({"label": option, "value": ix})

input_configuration = dbc.FormGroup(
    [
        dbc.Label("Input configuration"),
        dbc.Select(
            id="input-config",
            value=0,
            options=input_config_options,
            persistence=True,
            persistence_type="session",
        ),
        dbc.Tooltip("Input configuration", target="input-config", placement="bottom",),
    ]
)

input_coupling_options = []
for ix, option in enumerate(sr830.sr830().input_couplings):
    input_coupling_options.append({"label": option, "value": ix})

input_coupling = dbc.FormGroup(
    [
        dbc.Label("Input coupling"),
        dbc.Select(
            id="input-coupling",
            value=0,
            options=input_coupling_options,
            persistence=True,
            persistence_type="session",
        ),
        dbc.Tooltip("Input coupling", target="input-coupling", placement="bottom",),
    ]
)

input_grounding_options = []
for ix, option in enumerate(sr830.sr830().groundings):
    input_grounding_options.append({"label": option, "value": ix})

input_grounding = dbc.FormGroup(
    [
        dbc.Label("Input shield grounding"),
        dbc.Select(
            id="input-grounding",
            value=1,
            options=input_grounding_options,
            persistence=True,
            persistence_type="session",
        ),
        dbc.Tooltip(
            "Input shield grounding", target="input-grounding", placement="bottom",
        ),
    ]
)

line_notch_options = []
for ix, option in enumerate(sr830.sr830().input_line_notch_filter_statuses):
    line_notch_options.append({"label": option, "value": ix})

line_notch = dbc.FormGroup(
    [
        dbc.Label("Line notch filter status"),
        dbc.Select(
            id="line-notch",
            value=3,
            options=line_notch_options,
            persistence=True,
            persistence_type="session",
        ),
        dbc.Tooltip(
            "Line notch filter status", target="line-notch", placement="bottom",
        ),
    ]
)

ref_source_options = []
for ix, option in enumerate(sr830.sr830().reference_sources):
    ref_source_options.append({"label": option, "value": ix})

ref_source = dbc.FormGroup(
    [
        dbc.Label("Reference source"),
        dbc.Select(
            id="ref-source",
            value=0,
            options=ref_source_options,
            persistence=True,
            persistence_type="session",
        ),
        dbc.Tooltip(
            "Frequency reference source", target="ref-source", placement="bottom",
        ),
    ]
)

ref_trigger_options = []
for ix, option in enumerate(sr830.sr830().triggers):
    ref_trigger_options.append({"label": option, "value": ix})

ref_trigger = dbc.FormGroup(
    [
        dbc.Label("Reference trigger"),
        dbc.Select(
            id="ref-trigger",
            value=1,
            options=ref_trigger_options,
            persistence=True,
            persistence_type="session",
        ),
        dbc.Tooltip(
            "Frequency reference trigger", target="ref-trigger", placement="bottom",
        ),
    ]
)

ref_freq = dbc.FormGroup(
    [
        dbc.Label("Reference frequency (Hz)"),
        dbc.Input(
            id="ref_freq",
            type="number",
            value=1000,
            min=0.001,
            max=102000,
            step=0.001,
            persistence=True,
            persistence_type="session",
        ),
        dbc.FormFeedback("", valid=True),
        dbc.FormFeedback(
            "Reference frequency must be between 0.001 - 102000 Hz", valid=False
        ),
        dbc.Tooltip(
            "Internal reference output frequency",
            target="ref_freq",
            placement="bottom",
        ),
    ]
)

harmonic = dbc.FormGroup(
    [
        dbc.Label("Detection harmonic"),
        dbc.Input(
            id="harmonic",
            type="number",
            value=1,
            min=1,
            max=19999,
            step=1,
            persistence=True,
            persistence_type="session",
        ),
        dbc.FormFeedback("", valid=True),
        dbc.FormFeedback(
            "Detection harmonic must be between 1 - 19999 Hz", valid=False
        ),
        dbc.Tooltip("Detection harmonic", target="harmonic", placement="bottom",),
    ]
)


sensitivities = [
    "2 nV/V",
    "5 nV/V",
    "10 nV/V",
    "20 nV/V",
    "50 nV/V",
    "100 nV/V",
    "200 nV/V",
    "500 nV/V",
    "1 uV/V",
    "2 uV/V",
    "5 uV/V",
    "10 uV/V",
    "20 uV/V",
    "50 uV/V",
    "100 uV/V",
    "200 uV/V",
    "500 uV/V",
    "1 mV/V",
    "2 mV/V",
    "5 mV/V",
    "10 mV/V",
    "20 mV/V",
    "50 mV/V",
    "100 mV/V",
    "200 mV/V",
    "500 mV/V",
    "1 V/V",
]
if len(sensitivities) != len(sr830.sr830().sensitivities):
    raise ValueError

sensitivity_options = []
for ix, option in enumerate(sensitivities):
    sensitivity_options.append({"label": option, "value": ix})

sensitivity = dbc.FormGroup(
    [
        dbc.Label("Sensitivity"),
        dbc.Select(
            id="sensitivity",
            value=26,
            options=sensitivity_options,
            persistence=True,
            persistence_type="session",
        ),
        dbc.Tooltip("Input voltage gain", target="sensitivity", placement="bottom",),
    ]
)

reserve_mode_options = []
for ix, option in enumerate(sr830.sr830().reserve_modes):
    reserve_mode_options.append({"label": option, "value": ix})

reserve_mode = dbc.FormGroup(
    [
        dbc.Label("Reserve mode"),
        dbc.Select(
            id="reserve-mode",
            value=1,
            options=reserve_mode_options,
            persistence=True,
            persistence_type="session",
        ),
        dbc.Tooltip("Reserve mode", target="reserve-mode", placement="bottom",),
    ]
)


form = dbc.Form(
    [
        save_folder_input,
        dbc.Row(
            [dbc.Col(device_id_input, width=6), dbc.Col(interval_input, width=6)],
            form=True,
        ),
        dbc.Row(
            [dbc.Col(input_configuration, width=6), dbc.Col(input_coupling, width=6)],
            form=True,
        ),
        dbc.Row(
            [dbc.Col(input_grounding, width=6), dbc.Col(line_notch, width=6)], form=True
        ),
        dbc.Row(
            [dbc.Col(ref_source, width=6), dbc.Col(ref_trigger, width=6)], form=True
        ),
        dbc.Row([dbc.Col(ref_freq, width=6), dbc.Col(harmonic, width=6)], form=True),
        dbc.Row(
            [dbc.Col(sensitivity, width=6), dbc.Col(reserve_mode, width=6)], form=True
        ),
        html.Div(id="hidden", children="", hidden=True),
    ]
)

