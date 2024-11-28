import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import ppscore as pps
from feature_engine.discretisation import ArbitraryDiscretiser
from src.data_management import load_housing_data

sns.set_style("whitegrid")


def page_correlation_study_body():
    """
    Display correlated features and enable visual exploration of house price
    relationships with variables.
    """
    df = load_housing_data()

    vars_to_study = [
        '1stFlrSF', 'GarageArea', 'GrLivArea', 'KitchenQual',
        'MasVnrArea', 'OpenPorchSF', 'OverallQual',
        'TotalBsmtSF', 'YearBuilt', 'YearRemodAdd'
    ]

    st.write("### Housing Prices Correlation Study (BR1)")
    st.info(
        "* **BR1**: The client is interested in discovering correlations between house attributes and sale prices. "
        "This includes visualizing how various features relate to the target variable, `SalePrice`."
    )

    # Inspect the dataset
    if st.checkbox("Inspect Housing Data"):
        st.write(
            f"* The dataset contains {df.shape[0]} rows and {df.shape[1]} columns. "
            "Below are the first 10 rows of the dataset."
        )
        st.write(df.head(10))

    st.write("---")

    # Correlation study summary
    st.write(
        "* A correlation study was conducted to understand relationships between house features and `SalePrice`. "
        f"The most correlated features are: **{vars_to_study}**."
    )

    st.info(
        "* Key observations:\n"
        "    - Larger values for `1stFlrSF`, `GarageArea`, `GrLivArea`, `MasVnrArea`, and `TotalBsmtSF` "
        "tend to be associated with higher `SalePrice`.\n"
        "    - Recently built or remodeled houses (`YearBuilt`, `YearRemodAdd`) typically have higher prices.\n"
        "    - Features reflecting property quality (`KitchenQual`, `OverallQual`) are also positively correlated with `SalePrice`.\n"
        "    - However, relationships weaken at higher feature values, e.g., large `1stFlrSF` or `GarageArea` values."
    )

    df_eda = df[vars_to_study + ['SalePrice']]
    target_var = 'SalePrice'

    st.write("#### Data Visualizations")
    # Target variable distribution
    if st.checkbox("Distribution of Target Variable"):
        plot_target_hist(df_eda, target_var)

    # Visualize house prices per variable
    if st.checkbox("House Prices per Variable"):
        visualize_price_per_feature(df_eda, vars_to_study)

    # Correlation heatmaps
    if st.checkbox("Correlation Heatmaps (Pearson, Spearman, PPS)"):
        df_corr_pearson, df_corr_spearman, pps_matrix = calculate_corr_and_pps(df)
        display_corr_and_pps(
            df_corr_pearson, df_corr_spearman, pps_matrix,
            corr_threshold=0.4, pps_threshold=0.2
        )


def visualize_price_per_feature(df, features):
    """
    Generate plots (box, line, scatter) showing `SalePrice` trends for each feature.
    """
    time_features = ['YearBuilt', 'YearRemodAdd']
    target_var = 'SalePrice'

    for col in features:
        unique_values = len(df[col].unique())
        if unique_values <= 10:
            plot_box(df, col, target_var)
        elif col in time_features:
            plot_line(df, col, target_var)
        else:
            plot_reg(df, col, target_var)


def plot_target_hist(df, target_var):
    """Plot histogram of the target variable."""
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.histplot(data=df, x=target_var, kde=True, ax=ax)
    plt.title(f"Distribution of {target_var}", fontsize=20)
    st.pyplot(fig)


def plot_reg(df, col, target_var):
    """Generate scatter plot with regression line."""
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.regplot(data=df, x=col, y=target_var, ci=None, ax=ax)
    plt.title(f"Regression Plot: {target_var} vs {col}", fontsize=20)
    st.pyplot(fig)


def plot_line(df, col, target_var):
    """Generate line plot."""
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=df, x=col, y=target_var, ax=ax)
    plt.title(f"Line Plot: {target_var} vs {col}", fontsize=20)
    st.pyplot(fig)


def plot_box(df, col, target_var):
    """Generate box plot."""
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(data=df, x=col, y=target_var, ax=ax)
    plt.title(f"Box Plot: {target_var} vs {col}", fontsize=20)
    st.pyplot(fig)


def calculate_corr_and_pps(df):
    """Calculate Pearson, Spearman correlations and PPS matrix."""
    df_corr_pearson = df.corr(method="pearson")
    df_corr_spearman = df.corr(method="spearman")
    pps_matrix = pps.matrix(df).pivot(columns='x', index='y', values='ppscore')
    return df_corr_pearson, df_corr_spearman, pps_matrix


def display_corr_and_pps(df_corr_pearson, df_corr_spearman, pps_matrix, corr_threshold, pps_threshold):
    """Display correlation and PPS heatmaps."""
    st.write("##### Spearman Correlation Heatmap")
    heatmap_corr(df_corr_spearman, corr_threshold)

    st.write("##### Pearson Correlation Heatmap")
    heatmap_corr(df_corr_pearson, corr_threshold)

    st.write("##### PPS Heatmap")
    heatmap_pps(pps_matrix, pps_threshold)


def heatmap_corr(df, threshold, figsize=(12, 8)):
    """Create a heatmap for correlation data."""
    mask = np.triu(np.ones_like(df, dtype=bool))
    mask[np.abs(df) < threshold] = True

    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(df, annot=True, mask=mask, cmap='viridis', linewidths=0.5, ax=ax)
    st.pyplot(fig)


def heatmap_pps(df, threshold, figsize=(12, 8)):
    """Create a heatmap for PPS data."""
    mask = np.zeros_like(df, dtype=bool)
    mask[df < threshold] = True

    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(df, annot=True, mask=mask, cmap='rocket_r', linewidths=0.5, ax=ax)
    st.pyplot(fig)
