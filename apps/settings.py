"""Setup page."""

import dash_bootstrap_components as dbc
import sr830


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
            options=ref_trigger_options,
            persistence=True,
            persistence_type="session",
        ),
        dbc.Tooltip(
            "Frequency reference trigger", target="ref-trigger", placement="bottom",
        ),
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
    ]
)


layout = [form]
