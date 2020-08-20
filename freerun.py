"""Perform free-running measurements with an SRS SR830 lock-in amplifier."""
import argparse
import csv
import math
import pathlib
import statistics
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


def wait_for_lia_to_settle(lockin, timeout):
    """Wait for lock-in amplifier to settle.

    Parameters
    ----------
    lockin : lock-in amplifier object
        Lock-in amplifier object.
    timeout : float
        Maximum time to wait for lock-in to settle before moving on.

    Returns
    -------
    R : float
        Mean sampled R value after settling. Taking the mean of a sample reduces
        influence of noise.
    """
    lockin.reset_data_buffers()
    lockin.start()
    time.sleep(0.1)
    lockin.pause()
    R = lockin.get_ascii_buffer_data(1, 0, lockin.buffer_size)
    old_mean_R = statistics.mean(R)
    # if first measurement is way below the range, don't wait to settle
    if old_mean_R * 100 > lockin.sensitivities[lockin.sensitivity]:
        t_start = time.time()
        while True:
            if time.time() - t_start > timeout:
                print("Timed out waiting for signal to settle.")
                # init new_mean_R in case timeout is 0
                new_mean_R = old_mean_R
                break
            else:
                lockin.reset_data_buffers()
                lockin.start()
                time.sleep(0.1)
                lockin.pause()
                R = lockin.get_ascii_buffer_data(1, 0, lockin.buffer_size)
                new_mean_R = statistics.mean(R)
                if math.isclose(old_mean_R, new_mean_R, rel_tol=0.1):
                    break
                old_mean_R = new_mean_R
    else:
        new_mean_R = old_mean_R

    return new_mean_R


def custom_autogain(lia, timeout):
    """Find optimal gain setting.

    Parameters
    ----------
    lia : sr830 object
        Lock-in amplifier object.
    timeout : float
        Maximum time to wait for lock-in to settle before moving on.
    """
    while True:
        # get current sensitivity (both int and V/A)
        old_sensitivity = lia.sensitivity
        old_sensitivity_va = lia.sensitivities[old_sensitivity]

        # adjust sensitivity if R is not within 20 - 80 % of current range and not at
        # one high or low limit
        R = wait_for_lia_to_settle(lia, timeout)
        if (R >= old_sensitivity_va * 0.8) and (old_sensitivity < 26):
            new_sensitivity = old_sensitivity + 1
        elif (R <= 0.2 * old_sensitivity_va) and (old_sensitivity > 0):
            new_sensitivity = old_sensitivity - 1
        else:
            # found correct senstivity
            lia.sensitivity = old_sensitivity
            break

        # update sensitivity
        lia.sensitivity = new_sensitivity


def measure_all(lia, config, timeout):
    """Measure all lock-in parameters.

    Parameters
    ----------
    lia : sr830 object
        Lock-in amplifier object.
    config : dict
        Configuration dictionary.
    timeout : float
        Maximum time to wait for lock-in to settle before moving on.

    Returns
    -------
    data : list
        List of measured parameters
    """
    # set gain if required
    if config["auto_gain"] is True:
        if config["auto_gain_method"] == "instrument":
            lia.auto_gain()
            wait_for_lia_to_settle(lia, timeout)
        elif config["auto_gain_method"] == "custom":
            custom_autogain(lia)
        else:
            raise ValueError(
                f"Invalid auto-gain method: {config['auto_gain_method']}. Must be "
                + "'instrument' or 'custom'."
            )

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
with sr830.sr830() as lia:
    setup = config["lia"]["setup"]

    # connect to the instrument
    lia.connect(output_interface=setup["output_interface"], **config["lia"]["visa"])

    # setup the instrument
    lia.input_configuration = setup["input_configuration"]
    lia.input_coupling = setup["input_coupling"]
    lia.input_shield_grounding = setup["input_shield_grounding"]
    lia.line_notch_filter_status = setup["line_notch_filter_status"]
    lia.reference_source = setup["reference_source"]
    if config["reference_source"] == 1:
        # set frequency if using internal reference source
        lia.reference_frequency = setup["reference_frequency"]
    lia.reference_trigger = setup["reference_trigger"]
    lia.harmonic = setup["harmonic"]
    if lia.reference_frequency < 200:
        lia.sync_filter_status = 1
    lia.reserve_mode = setup["reserve_mode"]
    lia.time_constant = setup["time_constant"]
    lia.lowpass_filter_slope = setup["lowpass_filter_slope"]
    lia.set_display(1, setup["ch1_display"], setup["ch1_ratio"])
    lia.set_display(2, setup["ch2_display"], setup["ch2_ratio"])

    if setup["auto_gain"] is False:
        # user defined sensitivity setting
        lia.sensitivity = setup["sensitivity"]
    else:
        # set sensitivity/gain to lowest setting to prevent overload before autogain
        lia.sensitivity = 26

    # init save file
    header = (
        "timestamp (s)\tX (V)\tY (V)\tAux In 1 (V)\tAux In 2 (V)\tAux In 3 (V)\t"
        + "Aux In 4 (V)\tR (V)\tPhase (deg)\tFreq (Hz)\tCh1 display\tCh2 display\n"
    )

    save_path = pathlib.Path(args.save_path)
    if save_path.exists():
        i = (
            input(f"{save_path} already exists. Do you want to append to it? [y/n] ")
            or "y"
        )

        if i == "y":
            print("Appending to file...")
        elif i != "n":
            raise ValueError(f"Invalid input: '{i}'.")
    else:
        with open(save_path, "w", newline="\n") as f:
            f.writelines(header)

    # perform measurements and save data to file forever
    while True:
        data = measure_all(lia, config, setup["settling_timeout"])

        # append new data to save file
        with open(save_path, "a", newline="\n") as f:
            writer = csv.writer(f, delimiter="\t")
            writer.writerow(data)

        time.sleep(config["interval"])
