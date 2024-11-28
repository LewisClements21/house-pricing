import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.data_management import load_housing_data, load_pkl_file
from src.machine_learning.evaluate_reg import regression_performance, regression_evaluation_plots


def page_ml_predict_price_body():
    """
    Display the ML pipeline, feature importance, and performance metrics for house price prediction.
    """
    # Load files for the pipeline
    version = 'v4'
    base_path = f"outputs/ml_pipeline/predict_price/{version}/"
    price_pipe = load_pkl_file(f"{base_path}regression_pipeline.pkl")
    price_feat_importance = plt.imread(f"{base_path}features_importance.png")
    X_train = pd.read_csv(f"{base_path}X_train.csv")
    X_test = pd.read_csv(f"{base_path}X_test.csv")
    y_train = pd.read_csv(f"{base_path}y_train.csv")
    y_test = pd.read_csv(f"{base_path}y_test.csv")

    st.write("### ML Pipeline: Predict House Price")    

    # Display pipeline summary
    st.info(
        "* **BR2:** To meet the business requirement, we trained a regressor model to achieve at least "
        "0.75 accuracy in predicting house sale prices based on attributes.\n"
        "* The best pipeline achieved an R2 of 0.84 on the training set and 0.77 on the test set.\n"
        "* Below, we outline the pipeline steps, feature importance, and performance metrics."
    )
    st.write("---")

    # Show pipeline steps
    st.write("* **Pipeline Steps:**")
    st.code(price_pipe)
    st.write("---")

    # Show feature importance
    st.write("* **Features and Their Importance:**")
    st.write(X_train.columns.tolist())
    st.image(price_feat_importance)
    st.write("---")

    # Display pipeline performance
    st.write("### Pipeline Performance")
    st.write(
        "* **Performance Goal:** Achieve an R2 score of at least 0.75 on both the training and test sets.\n"
        "* **Results:** The model meets the performance criteria."
    )
    regression_performance(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test, pipeline=price_pipe)

    # Show regression performance plots
    st.write("### Regression Performance Plots")
    st.write(
        "* The plots below indicate that the model predicts house sale prices accurately for most cases. "
        "However, predictions are less reliable for houses with very high sale prices."
    )
    regression_evaluation_plots(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test, pipeline=price_pipe)
