library(nlme)

estimate_loa <- function(df) {
    start_time <- Sys.time()
    print("Start fitting model")

    # Test without adding the variance heterogeneity liberty
    #fm0 <- lme(sc ~ random_group + connection_index, random = list( connection_index = pdIdent( ~ random_group-1 ) ), data=df)
    fm1 <- lme(sc ~ random_group + connection_index, random = list( connection_index = pdIdent( ~ random_group-1 ) ), weights = varIdent( form = ~1 | random_group), data=df)

    end_time <- Sys.time()
    print(paste("Model fitted after that much time:", end_time - start_time))
    #summary(fm1)

    # Check model fit
    visualize_lmer_fit(fm1)

    # Extract values from fm1
    stddev_random_group_fm1 <- as.numeric(VarCorr(fm1)[1, "StdDev"])
    stddev_residual_fm1 <- as.numeric(VarCorr(fm1)["Residual", "StdDev"])
    fixed_effect_random_group_fm1 <- fixef(fm1)["random_group"]

    # # Extract values from fm0
    # stddev_random_group_fm0 <- as.numeric(VarCorr(fm0)[1, "StdDev"])
    # stddev_residual_fm0 <- as.numeric(VarCorr(fm0)["Residual", "StdDev"])
    # fixed_effect_random_group_fm0 <- fixef(fm0)["random_group"]

    # Compare allowing or not the residual variance to be different for each level of random_group
    # print(paste("fm1 - StdDev Random Group:", stddev_random_group_fm1, 
    #             "fm0 - StdDev Random Group:", stddev_random_group_fm0))
    # print(paste("fm1 - StdDev Residual:", stddev_residual_fm1, 
    #             "fm0 - StdDev Residual:", stddev_residual_fm0))
    # print(paste("fm1 - Fixed Effect Random Group:", fixed_effect_random_group_fm1, 
    #             "fm0 - Fixed Effect Random Group:", fixed_effect_random_group_fm0))


    log_ratio <- coef(fm1$modelStruct$varStruct)[1]
    multpl_var <- exp(log_ratio)

    # Compute the width of the limits of agreement (LoA)
    loa_diff <- 2 * sqrt(2*stddev_random_group_fm1^2+stddev_residual_fm1^2+(multpl_var*stddev_residual_fm1)^2)

    # Create a dataframe with loa_diff and bias
    loa_df <- data.frame(loa_diff = loa_diff, bias = fixed_effect_random_group_fm1)


    return(list(loa_df = loa_df, fm1 = fm1))
}

# Helper function to diagnose linear mixed-effects model fit
visualize_lmer_fit <- function(model, subplot_num = "A.", figure_title= ""){
    # Install and load necessary packages
    library(ggplot2)
    library(grid)
    library(gridExtra)
    library(ggpubr)

    #Plot size
    options(repr.plot.width=15, repr.plot.height=10)

    # Extract residuals and fitted values
    residuals <- residuals(model)
    fitted_values <- fitted(model)

    # Extract random effects
    random_effects_list <- ranef(model)

    # Residuals vs Fitted Values plot
    residuals_plot <- ggplot(data = data.frame(Fitted = fitted_values, Residuals = residuals),
                            aes(x = Fitted, y = Residuals)) +
        geom_point() +
        geom_hline(yintercept = 0, linetype = "dashed", color = "red") +
        theme(text = element_text(size = 46))+
        theme_minimal() +
        theme(plot.margin = unit(c(10,2,2,10), "mm")) +
        labs(title = "Residuals vs Fitted Values",
            x = "Fitted Values",
            y = "Residuals")

    # QQ plot of residuals
    qq_plot_residuals <- ggqqplot(residuals) +
        theme(text = element_text(size = 46))+
        theme_minimal() +
        theme(plot.margin = unit(c(10,10,2,2), "mm")) +
        labs(title = "Q-Q Plot of Residuals",
            x = "Theoretical Quantiles",
            y = "Sample Quantiles")    
    
    # Generate QQ plots for each random effect
    qq_plots_random_effects <- list()
    i <- 1
    for (re in names(random_effects_list)) {
        random_effects <- unlist(random_effects_list[[re]])
        qq_plot <- ggqqplot(random_effects) +
            theme(text = element_text(size = 46))+
            theme_minimal() +
            labs(title = paste("Q-Q Plot of Random Effects:", re),
                x = "Theoretical Quantiles",
                y = "Sample Quantiles")

        if (i%%2) {
            qq_plot <- qq_plot +
                theme(plot.margin = unit(c(2,2,10,10), "mm"))
        } else {
            qq_plot <- qq_plot +
                theme(plot.margin = unit(c(2,10,10,2), "mm"))
        }
                    
        qq_plots_random_effects[[re]] <- qq_plot
        i <- i + 1
    }
  
    # Combine all plots into a single figure
    combined_plots <- list(residuals_plot, qq_plot_residuals)
    combined_plots <- c(combined_plots, qq_plots_random_effects)
    combined_plot <- do.call(grid.arrange, c(combined_plots, ncol = 2))

    title_grob <- textGrob(figure_title, gp=gpar(fontsize=20))

    final_plot <- arrangeGrob(top= title_grob, combined_plot, ncol = 1)


    # Print the combined plot
    print(final_plot)

    return(final_plot)
}
