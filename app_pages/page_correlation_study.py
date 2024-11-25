import streamlit as st
from src.data_management import load_housing_data
import matplotlib.pyplot as plt
import seaborn as sns
import ppscore as pps
sns.set_style("whitegrid")
from feature_engine.discretisation import ArbitraryDiscretiser
import numpy as np
import plotly.express as px

def page_correlation_study_body():
    """
    Display correlated features and a checkbox to show the show
    house price per variable.
    """
    df = load_housing_data()

    vars_to_study = ['1stFlrSF', 'GarageArea', 'GrLivArea', 'KitchenQual', 'MasVnrArea', 'OpenPorchSF', 'OverallQual', 'TotalBsmtSF', 'YearBuilt', 'YearRemodAdd']

    st.write("### Housing Prices Correlation Study (BR1)")
    st.info(
        f"* **BR1** - The client is interested in discovering how house attributes correlate with sale prices.\
             Therefore, the client expects data visualizations of the correlated variables against the sale price. "
    )

    # inspect data
    if st.checkbox("Inspect Housing Data"):
        st.write(
            f"* The dataset has {df.shape[0]} rows and {df.shape[1]} columns.\
                 We show the first 10 rows below.\n"
            f"* SalePrice is our target variable, and we want to identify features correlated to it.")
        
        st.write(df.head(10))

    st.write("---")


    # Correlation Study Summary
    st.write(
        f"* We conducted a correlation study the notebook to better understand how "
        f"the variables are correlated to sale price of a property.\
         This addresses the first business requirement (BR1) of the project. \n"
        f"* We found that the most correlated variable are:\n **{vars_to_study}**"
    )


    # Text based on "03 - Correlation_Study" notebook - "Conclusions and Next steps" section
    st.info(
        f"We make the following observations from both the correlation analysis and the plots (particularly the heatmaps below).\n"
        f"* Higher values of 1stFlrSF, GarageArea, GrLivArea, MasVnrArea and TotalBsmtSF are associated with higher sale price.\n"
        f"* Recently built houses (YearBuilt) and houses with recently added remodel (YearRemodAdd) have typically higher prices.\n"  
        f"* Features that represent the quality of a property (KitchenQual and OverallQual) are also positively correlated to sale price of a house.\n\n" 
        f"While the plots corroborate these observations, we also note,\
         from the plots of sale price against the correlated features,\
         that the relationships become less clear at higher values of the variables.\n"
        f"* When the size of 1stFlrSF is around 2500, for example, sale price can be low or it can be very high.\n"
        f"* We see similar pattern in the regression plot of sale price and GarageArea when the latter's value is around 800.\n"
    )


    df_eda = df.filter(vars_to_study + ['SalePrice'])
    target_var = 'SalePrice'
    st.write("#### Data visualizations")
    # Distribution of target variable
    if st.checkbox("Distribution of Variable"):
        plot_target_hist(df_eda, target_var) 

    # Individual plots per variable
    if st.checkbox("House Prices per Variable"):
        house_price_per_variable(df_eda)
    

    if st.checkbox("Heatmaps: Pearson, Spearman and PPS Correlations"):
        df_corr_pearson, df_corr_spearman, pps_matrix = CalculateCorrAndPPS(df)
        DisplayCorrAndPPS(df_corr_pearson = df_corr_pearson,
                  df_corr_spearman = df_corr_spearman, 
                  pps_matrix = pps_matrix,
                  CorrThreshold = 0.4, PPS_Threshold =0.2,
                  figsize=(12,10), font_annot=10)


def house_price_per_variable(df_eda):
    """
    Generate box plot, line plot or scatter plot of SalePrice and
    the house features 
    """
    vars_to_study = ['1stFlrSF', 'GarageArea', 'GrLivArea', 'KitchenQual', 'MasVnrArea', 'OpenPorchSF', 'OverallQual', 'TotalBsmtSF', 'YearBuilt', 'YearRemodAdd']
    time = ['YearBuilt', 'YearRemodAdd']
    target_var = 'SalePrice'
    
    for col in vars_to_study:
        if len(df_eda[col].unique()) <= 10:
            plot_box(df_eda, col, target_var)
            print("\n\n")
        else:
            if col in time:
                plot_line(df_eda, col, target_var)
                print("\n\n")
            else:
                plot_reg(df_eda, col, target_var)
                print("\n\n")

def plot_target_hist(df, target_var):
  """
  Function to plot a histogram of the target variable
  """
  fig, axes = plt.subplots(figsize=(12, 6))
  sns.histplot(data=df, x=target_var, kde=True)
  plt.title(f"Distribution of {target_var}", fontsize=20)       
  st.pyplot(fig)

def plot_reg(df, col, target_var):
    """
    Generate scatter plot
    """
    fig, axes = plt.subplots(figsize=(12, 6))
    sns.regplot(data=df, x=col, y=target_var, ci=None)
    plt.title(f"Regression plot of {target_var} against {col}", fontsize=20)        
    st.pyplot(fig) # st.pyplot() renders image, in notebook is plt.show()

def plot_line(df, col, target_var):
    """
    Generate line plot
    """
    fig, axes = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=df, x=col, y=target_var)
    plt.title(f"Line plot of {target_var} against {col}", fontsize=20)        
    st.pyplot(fig) # st.pyplot() renders image, in notebook is plt.show()

def plot_box(df, col, target_var):
    """
    Generate box plot
    """
    fig, axes = plt.subplots(figsize=(12, 6))
    sns.boxplot(data=df, x=col, y=target_var) 
    plt.title(f"Box plot of {target_var} against {col}", fontsize=20)
    st.pyplot(fig) # st.pyplot() renders image, in notebook is plt.show()

## Heatmaps

def heatmap_corr(df,threshold, figsize=(20,12), font_annot = 8):
  """
  Function to create heatmap using correlations.
  """
  if len(df.columns) > 1:
    mask = np.zeros_like(df, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    mask[abs(df) < threshold] = True

    fig, axes = plt.subplots(figsize=figsize)
    sns.heatmap(df, annot=True, xticklabels=True, yticklabels=True,
                mask=mask, cmap='viridis', annot_kws={"size": font_annot}, ax=axes,
                linewidth=0.5
                     )
    axes.set_yticklabels(df.columns, rotation = 0)
    plt.ylim(len(df.columns),0)
    st.pyplot(fig)


def heatmap_pps(df,threshold, figsize=(20,12), font_annot = 8):
    """
    Function to create heatmap using pps.
    """
    if len(df.columns) > 1:

      mask = np.zeros_like(df, dtype=np.bool)
      mask[abs(df) < threshold] = True

      fig, ax = plt.subplots(figsize=figsize)
      ax = sns.heatmap(df, annot=True, xticklabels=True,yticklabels=True,
                       mask=mask,cmap='rocket_r', annot_kws={"size": font_annot},
                       linewidth=0.05,linecolor='grey')
      
      plt.ylim(len(df.columns),0)
      st.pyplot(fig)


def CalculateCorrAndPPS(df):
  """
  Function to calculate correlations and pps.
  """
  df_corr_spearman = df.corr(method="spearman")
  df_corr_spearman.name = 'corr_spearman'
  df_corr_pearson = df.corr(method="pearson")
  df_corr_pearson.name = 'corr_pearson'

  pps_matrix_raw = pps.matrix(df)
  pps_matrix = pps_matrix_raw.filter(['x', 'y', 'ppscore']).pivot(columns='x', index='y', values='ppscore')

  pps_score_stats = pps_matrix_raw.query("ppscore < 1").filter(['ppscore']).describe().T
  print(pps_score_stats.round(3))

  return df_corr_pearson, df_corr_spearman, pps_matrix


def DisplayCorrAndPPS(df_corr_pearson, df_corr_spearman, pps_matrix,CorrThreshold,PPS_Threshold,
                      figsize=(20,12), font_annot=8 ):
  """
  Function to display the correlations and pps.
  """

  heatmap_corr(df=df_corr_spearman, threshold=CorrThreshold, figsize=figsize, font_annot=font_annot)

  heatmap_corr(df=df_corr_pearson, threshold=CorrThreshold, figsize=figsize, font_annot=font_annot)

  heatmap_pps(df=pps_matrix,threshold=PPS_Threshold, figsize=figsize, font_annot=font_annot)