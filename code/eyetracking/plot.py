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

from typing import Tuple

import matplotlib.pyplot as plt
import pandas as pd


PLT_FIGURE_WIDTH = 16


def plot_heatmap_coordinate(
    data: pd.DataFrame,
    density: bool = False,
    cbar: bool = False,
    screen_size: Tuple[int, int] = (800, 600),
) -> plt.Figure:
    """
    Plots a heatmap for eye tracking coordinates.

    Parameters
    ----------
    data : :obj:`pandas.DataFrame`
        The dataframe the plot will get data from.
    density : :obj:`bool`
        If `True`, a kernel density estimation is fit to show smooth frequencies.
    cbar : :obj:`bool`
        Plot a colorbar.

    Returns
    -------
    fig : :obj:`~matplotlib.pyplot.figure.Figure`
        The matplotlib figure handle

    """
    import seaborn as sns

    # Make the aspect ratio of the figure resemble the screen proportion
    fig = plt.figure(figsize=(
        PLT_FIGURE_WIDTH,
        PLT_FIGURE_WIDTH * (1 - 0.2 * cbar) * screen_size[1] / screen_size[0])
    )

    cmap = sns.color_palette("coolwarm", as_cmap=True)
    clip = ((0, screen_size[0]), (0, screen_size[1]))
    if density:

        sns.kdeplot(
            data=data,
            cmap=cmap,
            x="eye1_x_coordinate",
            y="eye1_y_coordinate",
            fill=True,
            cbar=cbar,
            clip=clip,
            thresh=0,
        )
    else:
        plt.hist2d(
            data["eye1_x_coordinate"],
            data["eye1_y_coordinate"],
            range=clip,
            bins=(screen_size[0] // 10, screen_size[1] // 10),
            cmap=cmap,
        )

    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.invert_yaxis()

    plt.xticks([], [])
    plt.yticks([], [])
    plt.xlabel("x coordinate [pixels]")
    plt.ylabel("y coordinate [pixels]")
    return fig
