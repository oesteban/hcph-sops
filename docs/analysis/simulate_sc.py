import numpy as np


def simulate_sc(atlas_dim, scale, shape, num_sessions):
    """
    Simulate structural connectivity (SC) matrices.
    This function generates a reference SC matrix using a log-normal distribution
    and creates multiple noisy copies to simulate between-session variability.
    Parameters:
    -----------
    atlas_dim : int
        The dimensionality of the brain atlas (number of regions).
    scale : float
        The scale parameter for the log-normal distribution used to generate
        the reference SC matrix.
    shape : float
        The shape parameter (standard deviation of the log-normal distribution)
        used to generate the reference SC matrix.
    num_sessions : int
        The number of simulated sessions (copies of the SC matrix with added noise).
    Returns:
    --------
    np.ndarray
        A 3D numpy array of shape (num_sessions, atlas_dim, atlas_dim) containing
        the simulated SC matrices.
    """
    ## Fix the random seed the same way as in the defacing registered report (RR)
    day = 231108  # day and time the journal published our HCPh stage 1 RR
    time = 105017
    random_seed = day + time
    np.random.seed(random_seed)

    ## Simulate a reference structural connectivity (SC) matrix

    # SC matrices typically follow a heavy-tailed distribution, with a few strong connections and many weak ones.
    # We thus use a log-normal distribution to simulate SC value.
    SC_matrix = np.random.lognormal(
        mean=np.log(scale), sigma=shape, size=(atlas_dim, atlas_dim)
    )

    # Make it symmetric
    SC_matrix = (SC_matrix + SC_matrix.T) / 2

    # Set diagonal to 0 (no self-connections)
    np.fill_diagonal(SC_matrix, 0)

    assert SC_matrix.shape == (atlas_dim, atlas_dim)

    ## Copy this matrix multiple time to simulate multiple sessions of the same subject
    ## Add noise in the copies to simulate between-session variability
    SC_matrices = np.zeros((num_sessions, atlas_dim, atlas_dim))

    # Identify the 20th percentile threshold for the connection values in the reference SC matrix
    percentile_20_threshold = np.percentile(SC_matrix[SC_matrix > 0], 20)

    # Add noise to each duplicate
    for i in range(num_sessions):
        noise = np.random.normal(loc=0, scale=0.0005, size=SC_matrix.shape)
        higher_noise = np.random.normal(loc=0, scale=0.002, size=SC_matrix.shape)

        # Apply higher noise to connections below the 20th percentile to simulate higher variability in weaker connections
        noise[SC_matrix <= percentile_20_threshold] += higher_noise[
            SC_matrix <= percentile_20_threshold
        ]

        SC_matrices[i, :, :] = SC_matrix + noise

        # SC cannot have negative values so if the value gets negative cast it to 0
        SC_matrices[i, :, :] = np.maximum(SC_matrices[i, :, :], 0)

    print(
        f"Simulated a series of {SC_matrices.shape[0]} SC matrices of shape: ({SC_matrices.shape[1]}x{SC_matrices.shape[2]})"
    )
    # Test whether the shape is as expected
    assert SC_matrices.shape == (num_sessions, atlas_dim, atlas_dim)

    return SC_matrices