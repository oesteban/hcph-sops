# Copyright 2023 The Axon Lab <theaxonlab@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# We support and encourage derived works from this project, please read
# about our expectations at
#
#     https://www.nipreps.org/community/licensing/
#
from __future__ import annotations

import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from ..eyetrackingrun import EyeTrackingRun


def plot_pupil_size(
    etrun : EyeTrackingRun,
) -> None:
    """
    Plots the time series of pupil size.

    Parameters
    ----------
    etrun : str, optional
        Specifies whether to plot for the "right" or "left" eye.

    Returns
    -------
    Optional[str]
        The path to the saved plot file.

    Examples
    --------
    >>> plot_pupil_size(eye="left")

    """

    t_axis = (etrun.samples.timestamp.values - etrun.start_time) * 1e-3

    plt.plot(
        t_axis,
        np.squeeze(
            [
                etrun.samples[f"eye{n}_pupil_size"].values
                for n in (1, 2)
                if f"eye{n}_pupil_size" in etrun.samples.columns
            ]
        ),
    )

    plt.xlabel("time [s]")
    plt.ylabel("pupil size [a.u.]")


def plot_coordinates_ts(
    self,
    eye: str = "right",
    save: bool = False,
    path_save: str = ".",
    filename: Optional[str] = None,
) -> Optional[str]:
    """
    Plots a time series of eye tracking coordinates.

    Parameters
    ----------
    eye : str, optional
        Specifies whether to plot for the "right" or "left" eye.
    save : bool, optional
        If True, the plot is saved to a file.
    path_save : str, optional
        Path to save the plot file.
    filename : str, optional
        Name of the saved plot file.

    Returns
    -------
    Optional[str]
        The path to the saved plot file.

    Example
    -------
    DwiSession4.plot_coordinates_ts(eye="left")
    """

    if filename is None:
        filename = f"sub-{self.participant:03d}_ses-{self.session:03d}_task-{self.task_name}_coordinates_ts.pdf"
    time_start = self.find_timestamp_message()
    self.samples.time[(self.samples.time <= 0)] = np.nan
    if eye == "right":
        self.samples.gx_right[
            (self.samples.gx_right < 0)
            | (self.samples.gx_right > self.screen_resolution[0])
        ] = np.nan
        self.samples.gy_right[
            (self.samples.gy_right < 0)
            | (self.samples.gy_right > self.screen_resolution[1])
        ] = np.nan

        fig, axs = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
        print(
            self.samples["time"].values[0:10] - time_start,
            self.samples["time"].values[-20:-1] - time_start,
        )
        axs[0].plot(
            self.samples["time"].values - time_start,
            self.samples["gx_right"],
            label="gx_right",
        )
        axs[1].plot(
            self.samples["time"].values - time_start,
            self.samples["gy_right"],
            label="gy_right",
        )
        axs[1].set_xlabel("time [ms]")
        axs[1].set_ylabel("x coordinate [pixels]")
        axs[1].set_ylabel("y coordinate [pixels]")

    elif eye == "left":
        self.samples.gx_left[
            (self.samples.gx_left < 0)
            | (self.samples.gx_left > self.screen_resolution[0])
        ] = np.nan
        self.samples.gy_left[
            (self.samples.gy_left < 0)
            | (self.samples.gy_left > self.screen_resolution[1])
        ] = np.nan

        fig, axs = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

        axs[0].plot(self.samples["time"], self.samples["gx_left"], label="gx_left")
        axs[0].set_ylabel("gx_left")
        axs[1].plot(self.samples["time"], self.samples["gy_left"], label="gy_left")
        axs[1].set_xlabel("timestamp")
        axs[1].set_ylabel("pupil area [pixels]")
        axs[0].set_xlim(self.samples["time"].iloc[0])

    else:
        print("Invalid eye argument")

    if save:
        plt.savefig(os.path.join(path_save, filename))
        plt.clf()

    return plt.gcf()


def plot_heatmap_coordinate_density(
    self,
    eye: str = "right",
    save: bool = False,
    path_save: str = ".",
    filename: Optional[str] = None,
) -> Optional[str]:
    """
    Plots a heatmap for eye tracking coordinates.

    Parameters
    ----------
    eye : str, optional
        Specifies whether to plot for the "right" or "left" eye.
    save : bool, optional
        If True, the plot is saved to a file.
    path_save : str, optional
        Path to save the plot file.
    filename : str, optional
        Name of the saved plot file.

    Returns
    -------
    Optional[str]
        The path to the saved plot file.

    Examples
    --------
    >>> DwiSession4.plot_heatmap_coordinate_density(eye="left", screen_resolution=(1024, 768))
    """

    if filename is None:
        filename = f"sub-{self.participant:03d}_ses-{self.session:03d}_task-{self.task_name}_heatmap.pdf"

    plt.rcParams["figure.figsize"] = [10, 6]
    cmap = sns.color_palette("coolwarm", as_cmap=True)

    if eye == "right":
        filtered_samples = self.samples[
            (self.samples["gx_right"] >= 0)
            & (self.samples["gx_right"] <= self.screen_resolution[0])
            & (self.samples["gy_right"] >= 0)
            & (self.samples["gy_right"] <= self.screen_resolution[1])
        ]

        sns.kdeplot(
            data=filtered_samples,
            x="gx_right",
            y="gy_right",
            cmap=cmap,
            fill=True,
            cbar=True,
            thresh=0,
        )
        plt.gca().invert_yaxis()
        plt.xlabel("right eye x coordinate [pixels]")
        plt.xlabel("right eye y coordinate [pixels]")
    elif eye == "left":
        filtered_samples = self.samples[
            (self.samples["gx_left"] >= 0)
            & (self.samples["gx_left"] <= self.screen_resolution[0])
            & (self.samples["gy_left"] >= 0)
            & (self.samples["gy_left"] <= self.screen_resolution[1])
        ]

        sns.kdeplot(
            data=filtered_samples,
            x="gx_left",
            y="gy_left",
            cmap=cmap,
            fill=True,
            cbar=True,
            thresh=0,
        )
        plt.gca().invert_yaxis()
        plt.xlabel("left eye x coordinate [pixels]")
        plt.xlabel("left eye y coordinate [pixels]")
    if save:
        plt.savefig(os.path.join(path_save, filename))
    return plt.gcf()


def plot_delta(
    self,
    save: Optional[bool] = False,
    path_save: Optional[str] = ".",
    filename: Optional[str] = "blink_durations.pdf",
) -> None:
    """
    Plot the distribution of blink durations.

    Parameters
    ----------
    save : bool, optional
        Whether to save the plot as an image (default is False).
    path_save : str, optional
        Path to the directory where the image will be saved (default is current directory).
    filename : str, optional
        Name of the saved image file (default is "blink_durations.png").

    Returns
    -------
    None
        Displays the plot or saves it.

    Notes
    -----
    This method the blink occurences over time.
    """
    time_start = self.find_timestamp_message()
    blinks = self.events[self.events["blink"] == True]
    blinks_start = blinks["start"].values
    blinks_end = blinks["end"].values
    timestamps = self.samples["time"].values

    blinks_array = np.zeros_like(timestamps, dtype=int)
    for start, end in zip(blinks_start, blinks_end):
        blinks_array[(timestamps >= start) & (timestamps <= end)] = 1
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps - time_start, blinks_array)
    plt.xlabel("Blink occurences over time")

    if save:
        output_filename = f"sub-{self.participant:03d}_ses-{self.session:03d}_task-{self.task_name}_{filename}"
        plt.savefig(os.path.join(path_save, output_filename))

    return plt.gcf()


def plot_heatmap_coordinate_histo(
    self,
    eye: str = "right",
    notebook: bool = True,
    save: bool = False,
    path_save: str = ".",
    filename: str = "heatmap.pdf",
    bins: int = 100,
) -> Optional[None]:
    """
    Plots a 2D histogram for eye tracking coordinates.

    Parameters
    ----------
    eye : str, optional
        Specifies whether to plot for the "right" or "left" eye.
    save : bool, optional
        If True, the plot is saved to a file.
    path_save : str, optional
        Path to save the plot file.
    filename : str, optional
        Name of the saved plot file.
    bins : int, optional
        Number of bins for the histogram.

    Returns
    -------
    None or str
        None if notebook is True, else the path to the saved plot file.

    Example
    -------
    >>> DwiSession4.plot_heatmap_coordinate_histo(eye="left", screen_resolution=(1024, 768), bins=50)

    Notes
    -----
    This method plots a 2D histogram for eye tracking coordinates.
    """

    plt.rcParams["figure.figsize"] = [10, 6]
    plt.figure(figsize=(10, 6))
    cmap = sns.color_palette("coolwarm", as_cmap=True)

    if eye == "right":
        filtered_samples = self.samples[
            (self.samples["gx_right"] >= 0)
            & (self.samples["gx_right"] <= self.screen_resolution[0])
            & (self.samples["gy_right"] >= 0)
            & (self.samples["gy_right"] <= self.screen_resolution[1])
        ]

        plt.hist2d(
            filtered_samples["gx_right"],
            filtered_samples["gy_right"],
            range=[[0, self.screen_resolution[0]], [0, self.screen_resolution[1]]],
            bins=bins,
            cmap=cmap,
        )

        plt.xlabel("right eye x coordinate [pixels]")
        plt.ylabel("right eye y coordinate [pixels]")

    elif eye == "left":
        filtered_samples = self.samples[
            (self.samples["gx_left"] >= 0)
            & (self.samples["gx_left"] <= self.screen_resolution[0])
            & (self.samples["gy_left"] >= 0)
            & (self.samples["gy_left"] <= self.screen_resolution[1])
        ]

        plt.hist2d(
            filtered_samples["gx_left"],
            filtered_samples["gy_left"],
            range=[[0, screen_resolution[0]], [0, self.screen_resolution[1]]],
            bins=bins,
            cmap=cmap,
        )

        plt.xlabel("left eye x coordinate [pixels]")
        plt.ylabel("left eye y coordinate [pixels]")

    else:
        print("Invalid eye argument")

    plt.gca().invert_yaxis()
    plt.xlim(0, self.screen_resolution[0])
    plt.ylim(0, self.screen_resolution[1])

    if save:
        output_filename = f"sub-{self.participant:03d}_ses-{self.session:03d}_task-{self.task_name}_{filename}"
        plt.savefig(os.path.join(path_save, output_filename))
    return plt.gcf()
