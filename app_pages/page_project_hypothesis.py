import streamlit as st
def page_project_hypothesis_body():
    st.write("### Project Hypothesis and Validation")
    # conclusions taken from "02 - Churned Customer Study" notebook 
    st.success(
        f"* One of the most important attributes that determine the sales price of a house is the property size. This can include the interior and exterior surface area of the property. We hypothesize that houses with a lot of space have higher prices.\n\n"
        
        f"* The ages of a house and its sales price might be related. Specifically, recently built houses are likely to have modern facilities and thus higher sales prices."
    )