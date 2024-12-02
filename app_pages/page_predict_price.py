import streamlit as st
import pandas as pd
from datetime import date
from src.data_management import load_housing_data, load_heritage_data, load_pkl_file
from src.machine_learning.predictive_analysis_ui import predict_price, predict_inherited_house_price

def page_predict_price_body():
    # Load model and features
    version = 'v4'
    regression_pipe = load_pkl_file(f"outputs/ml_pipeline/predict_price/{version}/regression_pipeline.pkl")
    house_features = pd.read_csv(f"outputs/ml_pipeline/predict_price/{version}/X_train.csv").columns.tolist()

    st.title("House Price Prediction Dashboard")

    st.subheader("Prediction for Inherited Houses")
    st.info(
        "*This section predicts the sale prices for the client's four inherited houses in Ames, Iowa.*"
    )

    # Predict sales prices for inherited houses
    inherited_houses = load_heritage_data()
    inherited_houses['TotalSF'] = (
        inherited_houses['TotalBsmtSF'] + inherited_houses['1stFlrSF'] + inherited_houses['2ndFlrSF']
    )

    # Calculate predicted prices using a loop to ensure each row is passed correctly
    predicted_prices = []
    for i in range(inherited_houses.shape[0]):
        row = inherited_houses.iloc[[i]]
        price = round(predict_inherited_house_price(row, house_features, regression_pipe))
        predicted_prices.append(price)

    inherited_houses['PredictedSalePrice'] = predicted_prices
    total_value = sum(predicted_prices)

    st.write("**Predicted Sale Prices for Inherited Houses:**")
    st.dataframe(inherited_houses[house_features + ['PredictedSalePrice']])
    st.write(f"**Total Predicted Value:** ${total_value:,.2f}")

    st.write("---")
    st.subheader("Live House Price Prediction")
    st.write("Use the interface below to input house features and predict the sale price.")

    # Input widget for live predictions
    X_live = draw_inputs_widgets()

    if st.button("Predict Sale Price"):
        predicted_price = predict_price(X_live, house_features, regression_pipe)
        
        if predicted_price is not None:
            st.success(f"The predicted sale price is **${predicted_price:,.2f}**.")

def draw_inputs_widgets():
    """Generates Streamlit input widgets for live house price prediction."""
    df = load_housing_data()
    df['TotalSF'] = df['TotalBsmtSF'] + df['1stFlrSF'] + df['2ndFlrSF']
    min_factor, max_factor = 0.4, 2.0

    st.write("### Enter House Features")

    features = {
        "GarageArea": ("Garage Area (sq ft)", 50),
        "GrLivArea": ("Above Ground Living Area (sq ft)", 50),
        "OverallQual": ("Overall Quality (1-10)", 1),
        "TotalBsmtSF": ("Total Basement Area (sq ft)", 50),
        "YearBuilt": ("Year Built", 1)
    }

    X_live = pd.DataFrame(index=[0])
    for feature, (label, step) in features.items():
        col_min = int(df[feature].min() * min_factor) if feature != "OverallQual" else 1
        col_max = (
            int(df[feature].max() * max_factor)
            if feature != "YearBuilt"
            else date.today().year
        )
        col_value = int(df[feature].median())
        X_live[feature] = st.number_input(
            label=label,
            min_value=col_min,
            max_value=col_max,
            value=col_value,
            step=step,
        )

    return X_live
