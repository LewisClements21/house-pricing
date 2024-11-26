import streamlit as st

def page_project_hypothesis_body():

    st.write("### Project Hypotheses and Validation")

    # conclusions taken from "03 - Correlation_Study" notebook 
    st.success(
       f"**H1 - Size matters.** We hypothesize that larger the property, the higher its sale price will be.\n"
        f"* **Correct.** From the correlation study results, we found that features that reflect the size of\
             a property were positively and moderately correlated with sale price.\n\n"
       
       f"**H2 - Quality matters.** Ratings of the quality and condition of the house would reflect its value,\
         and thus we suspect that higher quality ratings indicate higher sale price.\n"
        f"* **Correct.**  We used the correlation between sale price and the kitchen quality and overall quality\
             ratings to show that this is indeed the case.\n\n"
       
       f"**H3 - Time matters.** We expect that the value of a property will be significantly influenced by how\
         old the property is and/or whether it had any remodel added to it recently.\n"
        f"* **Correct.** We validated this hypothesis by studying the correlation between the sale price and\
             the years it was built and/or had a remodel added to it. Both features have moderate positive correlation with sale price.\n"
       )
        