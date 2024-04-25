import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedKFold
from sklearn.model_selection import GridSearchCV

from mriqc_learn.datasets import load_data
from mriqc_learn.models import preprocess as pp
from mriqc_learn.models.production import init_pipeline_xgboost, init_pipeline_naive

#Load the HCPh data
iqms_path = Path('./data/group_T1w.tsv')
manual_ratings_path = Path('./data/desc-ratings_T1w.tsv')

df_iqms = pd.read_csv(iqms_path, sep='\t')
df_manual_ratings = pd.read_csv(manual_ratings_path, sep='\t')

# Merge the two dataframes based on the filename
# Cannot handle two raters for now!
df = pd.merge(df_manual_ratings, df_iqms, left_on='subject', right_on='bids_name', how='inner')
assert all(df['subject'] == df['bids_name'])
# Move the column bids_name to the first column
df = df[['bids_name'] + [col for col in df.columns if col != 'bids_name']]
df.drop(columns=['subject'], inplace=True)

# Split the data
(train_x, train_y), (_, _) = load_data(df, seed=2978, split_strategy="none")

# Keep only the rating
train_y = np.array(train_y['rating']).reshape(-1, 1)

## Cross-validation of default regressor

# Define a splitting strategy
outer_cv = RepeatedKFold(n_splits=10, n_repeats=3)

print("Running cross-validation with XGBoost")
cv_scores = cross_val_score(
    init_pipeline_xgboost(),
    X=train_x,
    y=train_y,
    cv=outer_cv,
    scoring="neg_mean_absolute_error",
    n_jobs=-1,
)

## Naive regressor
print("Running cross-validation with naive regressor returning mean of target values")
cv_scores = cross_val_score(
    init_pipeline_naive(strategy='mean'),
    X=train_x,
    y=train_y,
    cv=outer_cv,
    scoring="neg_mean_absolute_error",
    n_jobs=-1,
)
cv_scores = np.absolute(cv_scores)
print('Mean baseline mean MAE: %.3f (%.3f)' % (cv_scores.mean(), cv_scores.std()) )

print("Running cross-validation with naive regressor returning median of target values")
cv_scores = cross_val_score(
    init_pipeline_naive(strategy='median'),
    X=train_x,
    y=train_y,
    cv=outer_cv,
    scoring="neg_mean_absolute_error",
    n_jobs=-1,
)
cv_scores = np.absolute(cv_scores)
print('Mean baseline median MAE: %.3f (%.3f)' % (cv_scores.mean(), cv_scores.std()) )

## Nested cross-validation

# Define the parameter grid for hyperparameter tuning
param_grid = {
    'model__learning_rate': [0.1, 0.01, 0.001],
    'model__max_depth': [3, 7],
    'model__n_estimators': [50, 70, 90],
    'model__eta': [0.1, 0.01],
    'model__subsample': [0.7, 1.0],
}

# Initialize the XGBoost pipeline
pipeline = init_pipeline_xgboost()

# Initialize the GridSearchCV with the pipeline, parameter grid, and scoring metric
grid_search = GridSearchCV(
    estimator=pipeline,
    param_grid=param_grid,
    scoring='neg_mean_absolute_error',
    cv=outer_cv,
    n_jobs=-1
)

print("Running nested-cross-validation of xgboost regressor.")
nested_score = cross_val_score(
    grid_search,
    X=train_x,
    y=train_y,
    cv=outer_cv,
    scoring='neg_mean_absolute_error',
    n_jobs=16,
)
print(f'Mean MAE of nested cross-validation: {nested_score.mean()}')



