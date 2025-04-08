import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def compute_loa(df):
    import statsmodels.formula.api as smf

    # Convert dataframe to long format
    df = df.melt(
        id_vars=["random_group", "replication"],
        var_name="connection_index",
        value_name="sc",
    )


def extract_mean_diff(df):
    # Compute all pairwise differences and means
    connections = df.columns.difference(["random_group", "replication"])
    df_comp = pd.DataFrame()
    for conn in connections:
        pairwise_diffs = []
        pairwise_means = []
        for i in range(len(df) - 1):
            for j in range(i + 1, len(df)):
                diff = df.iloc[i][conn] - df.iloc[j][conn]
                mean = (df.iloc[i][conn] + df.iloc[j][conn]) / 2
                pairwise_diffs.append(diff)
                pairwise_means.append(mean)
        temp_df = pd.DataFrame({
            "diff": pairwise_diffs,
            "mean": pairwise_means,
            "connection": [conn] * len(pairwise_diffs)
        })
        df_comp = pd.concat([df_comp, temp_df], ignore_index=True)

    return df_comp["mean"], df_comp["diff"]



def ba_plot(
    df=None,
    diff=None,
    mean=None,
    hue=None,
    title=None,
    point_size=50,
    bright_color="#0041C2",
    pale_color="#6495ED",
):
    """
    Generate a Bland-Altman plot

    Parameters:
        data (DataFrame, optional): A pandas DataFrame containing the data.
        diff (array-like, optional): Differences between pairs of measurements. Required if `data` is not provided.
        mean (array-like, optional): Mean values of the pairs of measurements. Required if `data` is not provided.
        hue (array-like or str, optional): Column name in `data` or array-like for grouping points by color.
        title (str, optional): Title of the plot.
        point_size (int, optional): Size of the points in the scatter plot.
        bright_color (str, optional): Bright color for points outside the limits of agreement.
        pale_color (str, optional): Pale color for points within the limits of agreement.
    """

    # Extract mean, diff vectors if dataframe was passed
    if df is not None and diff is None and mean is None:
        mean, diff = extract_mean_diff(df)

    # Calculate statistics
    mean_diff = np.mean(diff)
    
    if df is not None:
        loa_diff = compute_loa(df)
    else:
        sd_diff = np.std(diff, ddof=1)
        loa_diff = 1.96 * sd_diff  # THIS IS WRONG !! MEASURES ARE NOT INDEPENDENT

    loa_inf = mean_diff - loa_diff
    loa_sup = mean_diff + loa_diff

    # Ensure shapes match
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
        loa_sup,
        color=pale_color,
        linestyle="--",
        linewidth=1,
        alpha=0.6,
        label="Upper LoA",
    )
    plt.axhline(
        loa_inf,
        color=pale_color,
        linestyle="--",
        linewidth=1,
        alpha=0.6,
        label="Lower LoA",
    )

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
