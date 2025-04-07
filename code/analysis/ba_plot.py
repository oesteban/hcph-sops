import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def ba_plot(
    diff, mean, hue=None, title=None, point_size=50, bright_color="#0041C2", pale_color="#6495ED"
):
    """
    Generate a Bland-Altman plot

    Parameters:
        diff (array-like): Differences between pairs of measurements.
        mean (array-like): Mean values of the pairs of measurements.
        title (str): Title of the plot.
        point_size (int): Size of the points in the scatter plot.
        bright_color (str): Bright color for points outside the limits of agreement.
        pale_color (str): Pale color for points within the limits of agreement.
    """

    # Calculate statistics
    mean_mean = np.mean(mean)
    mean_diff = np.mean(diff)
    sd_diff = np.std(diff, ddof=1)
    la_diff = 1.96 * sd_diff ## THIS IS WRONG !! MEASURES ARE NOT INDEPENDENT

    la_inf = mean_diff - la_diff
    la_sup = mean_diff + la_diff

    # Assign colors based on limits of agreement
    # Assign binary categories based on limits of agreement
    #outlier_flag = np.where((diff < la_inf) | (diff > la_sup), 1, 0)
    assert mean.shape == diff.shape, f"Shapes of mean {mean.shape}, diff {diff.shape} must match"
    if hue is not None:
        assert hue.shape == diff.shape, f"Shapes of hue {hue.shape}, diff {diff.shape} must match"

    # Create the plot
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        x=mean,
        y=diff,
        hue=hue,
        s=point_size,
        legend=False,
    )

    
    # Add horizontal lines for zero-difference line, mean difference and limits of agreement
    plt.axhline(
        0, color="grey", linestyle="-", linewidth=1, label="Zero Difference"
    )
    plt.axhline(
        mean_diff, color="black", linestyle="--", linewidth=1, label="Mean Difference"
    )
    plt.axhline(
        la_sup,
        color=pale_color,
        linestyle="--",
        linewidth=1,
        alpha=0.6,
        label="Upper LoA",
    )
    plt.axhline(
        la_inf,
        color=pale_color,
        linestyle="--",
        linewidth=1,
        alpha=0.6,
        label="Lower LoA",
    )

    """
    # Add annotations for mean difference and limits of agreement
    plt.text(
        mean_mean - mean_mean * 0.2,  # Adjusted to depend on mean_diff
        la_sup,
        f"{la_sup:.2f}",
        color=bright_color,
        ha="right",
        va="center",
        fontsize=10,
    )
    plt.text(
        mean_mean + mean_mean * 0.2,
        la_inf,
        f"{la_inf:.2f}",
        color=bright_color,
        ha="left",
        va="center",
        fontsize=10,
    )
    plt.text(
        mean_mean,
        mean_diff,
        f"{mean_diff:.2f}",
        color="black",
        ha="center",
        va="center",
        fontsize=10,
    )
    """

    # Customize plot appearance
    plt.xlabel("Mean connection value ")
    plt.ylabel("Difference in connection value between pairs of sessions")
    plt.title(title if title else "", fontsize=16)

    # Remove outline of the plot
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["left"].set_visible(False)
    plt.gca().spines["bottom"].set_visible(False)

    plt.show()
