import streamlit as st
from src.data_management import load_housing_data
import seaborn as sns
import matplotlib.pyplot as plt

def page_correlation_study_body():
    df = load_housing_data()
    vars_to_study = ['1stFlrSF', 'GarageArea', 'GarageYrBlt', 'GrLivArea', 
                     'KitchenQual', 'MasVnrArea', 'OverallQual', 'TotalBsmtSF', 
                     'YearBuilt', 'YearRemodAdd']
    
    # Filter to include only columns that exist in the dataset
    vars_to_study = [col for col in vars_to_study if col in df.columns]

    st.write("### Housing Prices Correlation Study")
    st.info(
        f"* The client is interested in identifying the features that have strong correlation with "
        f"house prices so that she can maximize the sales revenue."
    )

    # Inspect data
    if st.checkbox("Inspect Housing Data"):
        st.write(
            f"* The dataset has {df.shape[0]} rows and {df.shape[1]} columns, "
            f"find below the first 10 rows."
        )
        st.write(df.head(10))
        
        st.write(
        f"* A correlation study was conducted in the notebook to better understand how "
        f"the variables are correlated to Churn levels. \n"
        f"The most correlated variable are: **{vars_to_study}**"
    )
    # Text based on "03 - House Prices" notebook - "Conclusions and Next steps" section
    st.info(
        f"We make the following observations from both the correlation analysis and the plots.\n"
        f"* Higher values of 1stFlrSF, garage area, GrLivArea, MasVnrArea and TotalBsmtSF are associated with higher sale price.\n"
        f"* Houses with recently built garages or recently added remods have higher prices than those of earlier ones.\n"  
        f"* Higher Overall quality indicates higher sale prices but kitchen quality does not show clear pattern.\n" 
    )



    df_eda = df.filter(vars_to_study + ['SalePrice'])

    # Individual plots per variable
    if st.checkbox("House Prices per Variable"):
        selected_var = st.selectbox("Select a variable to plot", vars_to_study)
        house_price_per_variable(df_eda, selected_var)


def house_price_per_variable(df_eda, selected_var):
    time = ['GarageYrBlt', 'YearBuilt', 'YearRemodAdd']
    target_var = 'SalePrice'

    # Handle missing values and non-numeric data
    if df_eda[selected_var].dtype == 'object':
        df_eda[selected_var] = df_eda[selected_var].astype('category').cat.codes

    if len(df_eda[selected_var].unique()) <= 10:
        plot_box(df_eda, selected_var, target_var)
    else:
        if selected_var in time:
            plot_line(df_eda, selected_var, target_var)
        else:
            plot_scatter(df_eda, selected_var, target_var)

def plot_scatter(df, col, target_var):
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.scatterplot(data=df, x=col, y=target_var, ax=ax)
    plt.title(f"{col} vs {target_var}", fontsize=20)
    st.pyplot(fig)

def plot_line(df, col, target_var):
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=df, x=col, y=target_var, ax=ax)
    plt.title(f"{col} vs {target_var}", fontsize=20)
    st.pyplot(fig)

def plot_box(df, col, target_var):
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.boxplot(data=df, x=col, y=target_var, ax=ax)
    plt.title(f"{col} vs {target_var}", fontsize=20)
    st.pyplot(fig)
