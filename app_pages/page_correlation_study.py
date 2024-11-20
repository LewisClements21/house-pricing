import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")
from feature_engine.discretisation import ArbitraryDiscretiser
import numpy as np
import plotly.express as px
def page_correlation_study_body():
    st.write("### Housing Prices Correlation Study")
    st.info(
        f"* The client is interested in identifying the features that have strong correlation with "
        f"house prices so that she can maximize the sales revenue."
    )