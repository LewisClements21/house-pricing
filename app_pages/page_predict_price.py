import streamlit as st
import pandas as pd
from src.data_management import load_housing_data, load_heritage_data, load_pkl_file
from src.machine_learning.predictive_analysis_ui import predict_price, predict_inherited_house_price 
def page_predict_price_body():
	
	# load predict tenure files
	version = 'v4'
	price_pipe = load_pkl_file(f"outputs/ml_pipeline/predict_price/v4/regression_pipeline.pkl")
	house_features = (pd.read_csv(f"outputs/ml_pipeline/predict_price/v4/X_train.csv")
					.columns
					.to_list()
					)
	st.write("### House Price Predictor")
	st.info(
        f"* The client is interested in determining sales prices of four houses. "
	)
	
	st.write(f"Predicting sales price of inheritted houses.")

	X_inheritted = load_heritage_data()
	st.write(X_inheritted.filter(house_features).head())
	
	for i in range(X_inheritted.shape[0]):
		predict_inherited_house_price(X_inheritted.iloc[[i,]], house_features, price_pipe)
		
	
	# Generate Live Data
	# check_variables_for_UI(tenure_features, churn_features, cluster_features)
	X_live = DrawInputsWidgets()
	# predict on live data
	if st.button("Run Predictive Analysis"): 
		price_prediction = predict_price(X_live, house_features, price_pipe)
		
		if price_prediction == 1:
			predict_price(X_live, house_features, price_pipe)
			
def check_variables_for_UI(house_features):
	st.write(f"* There are {len(house_features)} features for the UI: \n\n {house_features}")
def DrawInputsWidgets():
	# load dataset
	df = load_housing_data()
	percentageMin, percentageMax = 0.4, 2.0
    # we create input widgets only for 6 features	
	col1, col2, col3, col4 = st.columns(4)
	col5, col6, col7, col8 = st.columns(4)
	# We are using these features to feed the ML pipeline - values copied from check_variables_for_UI() result
		
	# create an empty DataFrame, which will be the live data
	X_live = pd.DataFrame([], index=[0]) 
	
	# from here on we draw the widget based on the variable type (numerical or categorical)
	# and set initial values
	with col1:
		feature = "GarageArea"
		st_widget = st.selectbox(
			label= feature,
			options= df[feature].unique()
			)
	X_live[feature] = st_widget
	with col2:
		feature = "GrLivArea"
		st_widget = st.selectbox(
			label= feature,
			options= df[feature].unique()
			)
	X_live[feature] = st_widget
	with col3:
		feature = "OverallQual"
		st_widget = st.number_input(
			label= feature,
			min_value= df[feature].min()*percentageMin,
			max_value= df[feature].max()*percentageMax,
			value= df[feature].median()
			)
	X_live[feature] = st_widget
	with col4:
		feature = "TotalBsmtSF"
		st_widget = st.selectbox(
			label= feature,
			options= df[feature].unique()
			)
	X_live[feature] = st_widget
	with col5:
		feature = "YearBuilt"
		st_widget = st.selectbox(
			label= feature,
			options= df[feature].unique()
			)
	X_live[feature] = st_widget
	# st.write(X_live)
	return X_live