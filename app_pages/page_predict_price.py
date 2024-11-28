import streamlit as st
import pandas as pd
from datetime import date
from src.data_management import load_housing_data, load_heritage_data, load_pkl_file
from src.machine_learning.predictive_analysis_ui import predict_price, predict_inherited_house_price


def page_predict_price_body():
    """
    Displays the ML model interface for predicting house sale prices,
    including inherited houses and custom predictions.
    """

    # Load pipeline and feature data
    version = 'v4'
    base_path = f"outputs/ml_pipeline/predict_price/{version}/"
    regression_pipe = load_pkl_file(f"{base_path}regression_pipeline.pkl")
    house_features = pd.read_csv(f"{base_path}X_train.csv").columns.tolist()

    # Display page title and context
    st.write("### Predicting Sales Price of Inherited Houses (BR2)")
    st.info(
        "* **BR2** - The client seeks to predict sale prices for their 4 inherited houses "
        "and any other house in Ames, Iowa."
    )

    # Predict sales prices for inherited houses
    st.write("#### Predicted Sales Prices for Inherited Houses")
    st.write("* See the `PredictedSalePrice` column in the table below.")
    X_inherited = load_heritage_data()
    X_inherited['TotalSF'] = X_inherited['TotalBsmtSF'] + X_inherited['1stFlrSF'] + X_inherited['2ndFlrSF']

    predicted_sale_price = [
        round(predict_inherited_house_price(X_inherited.iloc[[i]], house_features, regression_pipe))
        for i in range(X_inherited.shape[0])
    ]
    summed_price = sum(predicted_sale_price)
    X_inherited = X_inherited.filter(house_features)
    X_inherited['PredictedSalePrice'] = predicted_sale_price

    st.write(X_inherited.head())
    st.write(
        f"* **Summed Price:** **${summed_price}**\n"
        f"* **Features Used:** {X_inherited.columns[:-1].tolist()}\n"
        "The ML model successfully predicted the sale prices of the inherited houses, "
        "and the total value of the properties has been calculated."
    )
    st.write("---")

    # Custom house price predictor interface
    st.write("### House Price Predictor Interface (BR2)")
    st.write("#### Predict Sale Price for Another House")
    st.write("Provide the attribute values below and click 'Predict Sale Price'.")

    X_live = draw_inputs_widgets()

    if st.button("Predict Sale Price"):
        price_prediction = predict_price(X_live, house_features, regression_pipe)
        st.write(f"### Predicted Sale Price: **${round(price_prediction)}**")


def draw_inputs_widgets():
    """
    Creates input widgets for live prediction of house prices.
    """
    # Load dataset and preprocess
    df = load_housing_data()
    df['TotalSF'] = df['TotalBsmtSF'] + df['1stFlrSF'] + df['2ndFlrSF']
    percentage_min, percentage_max = 0.4, 2.0

    # Initialize input layout and live data frame
    cols = st.columns(4)
    X_live = pd.DataFrame([], index=[0])

    # Define feature inputs
    features = [
        ("GarageArea", cols[0], 50),
        ("GrLivArea", cols[1], 50),
        ("OverallQual", cols[2], 1, 10, 1),
        ("TotalBsmtSF", cols[3], 50),
        ("YearBuilt", cols[0], 1, date.today().year, 1),
    ]

    for feature, col, step, *range_override in features:
        with col:
            if range_override:
                min_value, max_value = range_override
            else:
                min_value = int(df[feature].min() * percentage_min)
                max_value = int(df[feature].max() * percentage_max)

            X_live[feature] = st.number_input(
                label=feature,
                min_value=min_value,
                max_value=max_value,
                value=int(df[feature].median()),
                step=step,
            )

    return X_live
