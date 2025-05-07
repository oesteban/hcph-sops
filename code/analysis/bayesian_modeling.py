import pymc as pm
import numpy as np
import arviz as az
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display


def generate_synthetic_data(
    true_pi0, true_lambda, true_mu, true_sigma, n_samples, random_seed=None
):
    """
    Generate synthetic data from a mixture model.

    Parameters:
    -----------
    true_pi0 : float
        Proportion of unconnected regions (0 to 1)
    true_lambda : float
        Rate parameter for exponential distribution (unconnected regions)
    true_mu : float
        Mean density for connected regions
    true_sigma : float
        Standard deviation for connected regions
    n_samples : int
        Number of samples to generate
    random_seed : int, optional
        Random seed for reproducibility

    Returns:
    --------
    tuple
        (density_values, connection_status, parameter_dict)
    """
    if random_seed is not None:
        np.random.seed(random_seed)

    # Randomly assign connection status (0 = not connected, 1 = connected)
    connection_status = np.random.binomial(1, 1 - true_pi0, size=n_samples)

    # Generate density values based on connection status
    density_values = np.zeros(n_samples)

    # For unconnected regions (exponential distribution)
    unconnected_idx = connection_status == 0
    density_values[unconnected_idx] = np.random.exponential(
        scale=1 / true_lambda,  # Convert rate to scale
        size=np.sum(unconnected_idx),
    )

    # For connected regions (truncated normal distribution)
    connected_idx = connection_status == 1
    # Generate normal values and clip at 0
    normal_values = np.random.normal(
        loc=true_mu, scale=true_sigma, size=np.sum(connected_idx)
    )
    # Cast negative values to zero
    density_values[connected_idx] = np.clip(normal_values, 0, None)

    # Create parameter dictionary for reference
    params = {
        "pi0": true_pi0,
        "lambda": true_lambda,
        "mu": true_mu,
        "sigma": true_sigma,
        "n_samples": n_samples,
    }

    return density_values, connection_status, params


def create_data_histogram(
    density_values,
    params,
    bins=50,
    title="Synthetic Density Data from Mixture Model",
    color="blue",
):
    """
    Create histogram of the synthetic data.

    Parameters:
    -----------
    density_values : array-like
        Synthetic density values
    params : dict
        Parameter dictionary
    bins : int, optional
        Number of histogram bins

    Returns:
    --------
    matplotlib.figure.Figure
        Figure with the histogram
    """
    fig = plt.figure(figsize=(10, 6))
    plt.hist(density_values, bins=bins, alpha=0.7, density=True, color=color)
    plt.axvline(
        x=params["mu"],
        color="red",
        linestyle="--",
        label=f"True mean for connected: {params['mu']}",
    )
    plt.title(title)
    plt.xlabel("Density")
    plt.ylabel("Frequency")
    plt.legend()
    return fig


def define_mixture_model(
    observed=None, mu_type="fixed", mu_value=0.8, mu_prior_mean=0.8, mu_prior_sigma=0.2
):
    with pm.Model() as model:
        # Prior for proportion of unconnected regions
        pi0 = pm.Beta("pi0", alpha=1, beta=1)

        # Prior for exponential rate parameter
        lambda_exp = pm.Gamma("lambda_exp", alpha=2, beta=3)

        # Prior for standard deviation of connected regions
        sigma = pm.HalfNormal("sigma", sigma=0.1)

        # Mean for connected regions - either fixed or learned
        if mu_type == "fixed":
            mu = mu_value  # Using fixed value
        else:  # "learned"
            mu = pm.Normal("mu", mu=mu_prior_mean, sigma=mu_prior_sigma)

        # Component 1: Exponential distribution for unconnected regions
        density_unconnected = pm.Exponential.dist(lam=lambda_exp)

        # Component 2: Truncated Normal for connected regions
        density_connected = pm.TruncatedNormal.dist(mu=mu, sigma=sigma, lower=0)

        # Mixture of the twos
        density = pm.Mixture(
            "density",
            w=[pi0, 1 - pi0],
            comp_dists=[density_unconnected, density_connected],
            observed=observed,
        )

        # Save the observed data for later use
        model_info = {
            "observed_data": observed,
            "mu_type": mu_type,
            "mu_value": mu_value if mu_type == "fixed" else None,
        }

    return model, model_info


def prior_preditive_sampling(
    params, mu_type="fixed", mu_value=0.8, mu_prior_mean=0.8, mu_prior_sigma=0.2, draws=100
):
    model, model_info = define_mixture_model(
        mu_type=mu_type,
        mu_value=mu_value,
        mu_prior_mean=mu_prior_mean,
        mu_prior_sigma=mu_prior_sigma,
    )
    with model:
        prior_samples = pm.sample_prior_predictive(draws=draws)

    fig = create_data_histogram(
        prior_samples.prior["density"].values.flatten(),
        params,
        title="Prior samples",
        color="orange",
    )
    return fig


def fit_mixture_model(
    density_values,
    mu_type="fixed",
    mu_value=0.8,
    mu_prior_mean=0.8,
    mu_prior_sigma=0.2,
    n_samples=2000,
    n_tune=1000,
    random_seed=None,
):
    """
    Fit PyMC mixture model to the data.

    Parameters:
    -----------
    density_values : array-like
        Density values to fit
    mu_type : str, optional
        How to handle the mu parameter: "fixed" or "learned"
    mu_value : float, optional
        Value to use if mu_type is "fixed"
    mu_prior_mean : float, optional
        Prior mean for mu if mu_type is "learned"
    mu_prior_sigma : float, optional
        Prior standard deviation for mu if mu_type is "learned"
    n_samples : int, optional
        Number of posterior samples
    n_tune : int, optional
        Number of tuning steps
    random_seed : int, optional
        Random seed for reproducibility

    Returns:
    --------
    tuple
        (arviz.InferenceData, pm.Model, dict)
    """
    # Load the model from define_mixture_model
    model, model_info = define_mixture_model(
        observed=density_values,
        mu_type=mu_type,
        mu_value=mu_value,
        mu_prior_mean=mu_prior_mean,
        mu_prior_sigma=mu_prior_sigma,
    )
    with model:
        # Sample from the posterior
        trace = pm.sample(
            n_samples,
            tune=n_tune,
            target_accept=0.9,
            return_inferencedata=True,
            random_seed=random_seed,
        )

    return trace, model, model_info


def create_analysis_plots(trace, params, model_info):
    """
    Create analysis plots without displaying them.

    Parameters:
    -----------
    trace : arviz.InferenceData
        Trace from the MCMC sampling
    params : dict
        True parameter values
    model_info : dict
        Information about the model and observed data

    Returns:
    --------
    dict
        Dictionary containing figures and summary statistics
    """
    results = {}

    # Get variables to summarize
    var_names = ["pi0", "sigma", "lambda_exp"]
    if model_info["mu_type"] == "learned":
        var_names.append("mu")

    # Summarize the results
    summary = az.summary(trace, var_names=var_names)
    results["summary"] = summary

    # Parameter comparison
    param_comparison = {}
    for param_name, pymc_name in [
        ("pi0", "pi0"),
        ("lambda", "lambda_exp"),
        ("sigma", "sigma"),
        ("mu", "mu"),
    ]:
        # Skip mu if it was fixed in the model
        if param_name == "mu" and model_info["mu_type"] == "fixed":
            param_comparison[param_name] = {
                "true": params[param_name],
                "estimated": model_info["mu_value"],
                "note": "Fixed parameter (not estimated)",
            }
        elif pymc_name in summary.index:
            true_val = params[param_name]
            posterior_mean = summary.loc[pymc_name, "mean"]
            param_comparison[param_name] = {
                "true": true_val,
                "estimated": posterior_mean,
            }
    results["param_comparison"] = param_comparison

    # Trace plot
    fig_trace = plt.figure(figsize=(12, 8))
    trace_plot = az.plot_trace(trace, var_names=var_names)
    if params:
        for ax, true_value in zip(
            trace_plot[:, 0].ravel(), [params["pi0"], params["sigma"], params["lambda"]]
        ):
            ax.axvline(
                true_value,
                color="red",
                linestyle="--",
                label=f"True value: {true_value}",
            )
        for ax, true_value in zip(
            trace_plot[:, 1].ravel(), [params["pi0"], params["sigma"], params["lambda"]]
        ):
            ax.axhline(
                true_value,
                color="red",
                linestyle="--",
                label=f"True value: {true_value}",
            )
    plt.tight_layout()
    results["trace_plot"] = fig_trace

    # Energy plot
    fig_energy = plt.figure(figsize=(10, 6))
    az.plot_energy(trace)
    plt.tight_layout()
    results["energy_plot"] = fig_energy

    # Forest plot
    fig_forest = plt.figure(figsize=(10, 6))
    az.plot_forest(trace, var_names=var_names, combined=True, hdi_prob=0.95)
    plt.tight_layout()
    results["forest_plot"] = fig_forest

    # Autocorrelation plot
    fig_autocorr = plt.figure(figsize=(10, 10))
    az.plot_autocorr(trace, var_names=var_names)
    plt.tight_layout()
    results["autocorr_plot"] = fig_autocorr

    # Posterior predictive
    with pm.Model() as pp_model:
        # Prior for proportion of unconnected regions
        pi0 = pm.Beta("pi0", alpha=1, beta=1)

        # Prior for exponential rate parameter
        lambda_exp = pm.Gamma("lambda_exp", alpha=2, beta=3)

        # Prior for standard deviation of connected regions
        sigma = pm.HalfNormal("sigma", sigma=0.1)

        # Mean for connected regions - either fixed or learned
        if model_info["mu_type"] == "fixed":
            mu = model_info["mu_value"]
        else:
            mu = pm.Normal("mu", mu=0.8, sigma=0.2)

        # Component 1: Exponential distribution for unconnected regions
        density_unconnected = pm.Exponential.dist(lam=lambda_exp)

        # Component 2: Truncated Normal for connected regions
        density_connected = pm.TruncatedNormal.dist(mu=mu, sigma=sigma, lower=0)

        # Mixture model
        density = pm.Mixture(
            "density",
            w=[pi0, 1 - pi0],
            comp_dists=[density_unconnected, density_connected],
        )

        # Sample from the posterior predictive
        posterior_predictive = pm.sample_posterior_predictive(trace)

    # Create the posterior predictive plot
    fig_pp = plt.figure(figsize=(10, 6))
    plt.hist(
        model_info["observed_data"],
        bins=50,
        alpha=0.7,
        density=True,
        color="blue",
        label="Observed Data",
    )

    sns.kdeplot(
        posterior_predictive.posterior_predictive["density"].values.flatten(),
        color="red",
        label="Posterior Predictive",
    )

    plt.title("Data vs. Posterior Predictive Distribution")
    plt.xlabel("Density")
    plt.ylabel("Density")
    plt.legend()
    plt.tight_layout()
    results["posterior_predictive_plot"] = fig_pp

    return results


def run_simulation(
    true_pi0=0.3,
    true_lambda=2.0,
    true_mu=0.8,
    true_sigma=0.15,
    n_samples=2000,
    mu_type="fixed",
    mu_prior_mean=0.8,
    mu_prior_sigma=0.2,
    random_seed=42,
    display_plots=False,
):
    """
    Run a complete simulation and return results.

    Parameters:
    -----------
    true_pi0 : float
        Proportion of unconnected regions (0 to 1)
    true_lambda : float
        Rate parameter for exponential distribution (unconnected regions)
    true_mu : float
        Mean density for connected regions
    true_sigma : float
        Standard deviation for connected regions
    n_samples : int
        Number of samples to generate
    mu_type : str
        How to handle the mu parameter: "fixed" or "learned"
    mu_prior_mean : float
        Prior mean for mu if mu_type is "learned"
    mu_prior_sigma : float
        Prior standard deviation for mu if mu_type is "learned"
    random_seed : int
        Random seed for reproducibility
    display_plots : bool
        Whether to display plots immediately (otherwise they're just returned)

    Returns:
    --------
    dict
        Dictionary with all plots and results
    """
    results = {}

    print(f"Simulation with parameters:")
    print(f"- pi0 (proportion unconnected): {true_pi0}")
    print(f"- lambda (exponential rate): {true_lambda}")
    print(f"- mu (connected mean): {true_mu}")
    print(f"- sigma (connected std): {true_sigma}")
    print(f"- n_samples: {n_samples}")
    print(f"- mu_type: {mu_type}")
    if mu_type == "learned":
        print(f"- mu_prior_mean: {mu_prior_mean}")
        print(f"- mu_prior_sigma: {mu_prior_sigma}")
    print("-" * 50)

    # Generate data
    print("Generating synthetic data...")
    density_values, connection_status, params = generate_synthetic_data(
        true_pi0, true_lambda, true_mu, true_sigma, n_samples, random_seed
    )
    results["data"] = {
        "density_values": density_values,
        "connection_status": connection_status,
        "params": params,
    }

    # Create data histogram
    print("Creating data histogram...")
    data_fig = create_data_histogram(density_values, params)
    results["data_histogram"] = data_fig
    if display_plots:
        display(data_fig)

    # Prior predictive sampling
    print("Drawing prior predictive samples...")
    mu_value = true_mu if mu_type == "fixed" else None
    prior_fig = prior_preditive_sampling(
        params,
        mu_type=mu_type,
        mu_value=mu_value,
        mu_prior_mean=mu_prior_mean,
        mu_prior_sigma=mu_prior_sigma,
        draws=1000,
    )
    results["prior_sampling_histogram"] = prior_fig
    if display_plots:
        display(priors_fig)

    # Fit model
    print("Fitting PyMC model (this may take a few minutes)...")
    trace, model, model_info = fit_mixture_model(
        density_values,
        mu_type=mu_type,
        mu_value=mu_value,
        mu_prior_mean=mu_prior_mean,
        mu_prior_sigma=mu_prior_sigma,
        n_samples=2000,
        n_tune=1000,
        random_seed=random_seed,
    )
    results["trace"] = trace
    results["model_info"] = model_info

    # Create analysis plots
    print("Creating analysis plots...")
    analysis_results = create_analysis_plots(trace, params, model_info)
    results.update(analysis_results)

    if display_plots:
        print("\nSummary statistics:")
        display(analysis_results["summary"])

        print("\nParameter comparison:")
        for param, values in analysis_results["param_comparison"].items():
            if "note" in values:
                print(
                    f"{param}: True = {values['true']:.3f}, Value = {values['estimated']:.3f} ({values['note']})"
                )
            else:
                print(
                    f"{param}: True = {values['true']:.3f}, Estimated = {values['estimated']:.3f}"
                )

        print("\nDiagnostic plots:")
        display(analysis_results["trace_plot"])
        display(analysis_results["energy_plot"])
        display(analysis_results["forest_plot"])
        display(analysis_results["autocorr_plot"])

        if "posterior_predictive_plot" in analysis_results:
            print("\nPosterior predictive check:")
            display(analysis_results["posterior_predictive_plot"])

    return results


def display_simulation_results(results):
    """
    Display all plots and results from a previously run simulation.

    Parameters:
    -----------
    results : dict
        Dictionary with simulation results
    """
    print("Simulation results:")
    print("-" * 50)

    print("\nParameter values:")
    params = results["data"]["params"]
    for param, value in params.items():
        print(f"- {param}: {value}")

    print("\nSummary statistics:")
    display(results["summary"])

    print("\nParameter comparison:")
    for param, values in results["param_comparison"].items():
        if "note" in values:
            print(
                f"{param}: True = {values['true']:.3f}, Value = {values['estimated']:.3f} ({values['note']})"
            )
        else:
            print(
                f"{param}: True = {values['true']:.3f}, Estimated = {values['estimated']:.3f}"
            )

    print("\nData histogram:")
    display(results["data_histogram"])

    print("\nTrace plot:")
    display(results["trace_plot"])

    print("\nEnergy plot:")
    display(results["energy_plot"])

    print("\nForest plot:")
    display(results["forest_plot"])

    print("\nAutocorrelation plot:")
    display(results["autocorr_plot"])

    if "posterior_predictive_plot" in results:
        print("\nPosterior predictive check:")
        display(results["posterior_predictive_plot"])
