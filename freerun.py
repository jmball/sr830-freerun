"""Perform free-running measurements with an SRS SR830 lock-in amplifier."""
import argparse
import csv
import time

import sr830
import yaml

parser = argparse.ArgumentParser()
parser.add_argument(
    "-c",
    "--config-path",
    default="example_config.yaml",
    help="Path to configuration file (yaml format).",
)
parser.add_argument(
    "-s", "--save-path", default="temp.tsv", help="Path for save file (tsv format).",
)
args = parser.parse_args()


class csr830(sr830.sr830):
    """SR830 lock-in amplifier class that can be used with a context manager."""

    def __init__(self, return_int=False, check_errors=False):
        super().__init__(return_int, check_errors)

    def __enter__(self):
        """Enter the runtime context related to this object."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the runtime context related to this object.

        Make sure everything gets cleaned up properly.
        """
        self.set_sensitivity(26)
        self.disconnect()


def custom_autogain(lia):
    """Find optimal gain setting.

    Parameters
    ----------
    lia : sr830 object
        Lock-in amplifier object.
    """
    gain_set = False
    while not gain_set:
        # get current sensitivity
        sensitivity_int = lia.get_sensitivity()
        sensitivity = lia.sensitivities[sensitivity_int]

        # get current time constant
        time_constant_int = lia.get_time_constant()
        time_constant = lia.time_constants[time_constant_int]

        # wait 5 time constants for signal to settle
        time.sleep(5 * time_constant)

        # adjust sensitivity if R is not within 10 - 90 % of current range and not at
        # one high or low limit
        R = lia.measure(3)
        if (R >= sensitivity * 0.9) and (sensitivity_int < 26):
            new_sensitivity = sensitivity_int + 1
        elif (R <= 0.1 * sensitivity) and (sensitivity_int > 0):
            new_sensitivity = sensitivity_int - 1
        else:
            # found correct senstivity
            new_sensitivity = sensitivity_int
            gain_set = True

        # update sensitivity
        lia.set_sensitivity(new_sensitivity)


def measure_all(lia, config):
    """Measure all lock-in parameters.

    Parameters
    ----------
    lia : sr830 object
        Lock-in amplifier object.
    config : dict
        Configuration dictionary.

    Returns
    -------
    data : list
        List of measured parameters
    """
    # set gain if required
    if config["auto_gain"] is True:
        if config["auto_gain_method"] == "instrument":
            lia.auto_gain()
        elif config["auto_gain_method"] == "custom":
            custom_autogain(lia)
        else:
            raise ValueError(
                f"Invalid auto-gain method: {config['auto_gain_method']}. Must be "
                + "'instrument' or 'custom'."
            )

    # allow 5 time constants for signal to settle
    time_constant_int = lia.get_time_constant()
    time_constant = lia.time_constants[time_constant_int]
    time.sleep(5 * time_constant)

    # measure all available lock-in paramteres
    data0 = [time.time()]
    data1 = list(lia.measure_multiple([1, 2, 5, 6, 7, 8]))
    data2 = list(lia.measure_multiple([3, 4, 9, 10, 11]))

    return data0 + data1 + data2


# load the configuration file
with open(args.config, "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)


# run lock-in amplifier in context manager so it gets cleaned up properly if an error
# occurs
with csr830(return_int=True) as lia:
    # connect to the instrument
    lia.connect(
        config["resource_name"],
        config["output_interface"],
        reset=True,
        set_default_configuration=False,
    )

    # set configuration
    lia.set_input_configuration(config["input_configuration"])
    lia.set_input_coupling(config["input_coupling"])
    lia.set_input_shield_gnd(config["ground_shielding"])
    lia.set_line_notch_status(config["line_notch_filter_status"])
    lia.set_ref_source(config["ref_source"])
    if config["ref_source"] == 0:
        lia.set_ref_freq(config["ref_freq"])
    lia.set_harmonic(config["detection_harmonic"])
    lia.set_reference_trigger(config["ref_trigger"])
    lia.set_reserve_mode(config["reserve_mode"])
    lia.set_time_constant(config["time_constant"])
    lia.set_lp_filter_slope(config["low_pass_filter_slope"])
    lia.set_sync_status(config["sync_status"])
    lia.set_display(1, config["ch1_display"], config["ch1_ratio"])
    lia.set_display(2, config["ch2_display"], config["ch2_ratio"])

    if config["auto_gain"] is False:
        # user defined sensitivity setting
        lia.set_sensitivity(config["sensitivity"])
    else:
        # set sensitivity/gain to lowest setting to prevent overload before autogain
        lia.set_sensitivity(26)

    # init save file
    header = (
        "timestamp (s)\tX (V)\tY (V)\tAux In 1 (V)\tAux In 2 (V)\tAux In 3 (V)\t"
        + "Aux In 4 (V)\tR (V)\tPhase (deg)\tFreq (Hz)\tCh1 display\tCh2 display\n"
    )
    with open(args.save_path, "w", newline="\n") as f:
        f.writelines(header)

    # perform measurements and save data to file forever
    while True:
        data = measure_all(lia, config)

        # append new data to save file
        with open(args.save_path, "a", newline="\n") as f:
            writer = csv.writer(f, delimiter="\t")
            writer.writerow(data)

        time.sleep(config["interval"])
