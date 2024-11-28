import streamlit as st

def page_project_hypothesis_body():
    st.write("### Project Hypotheses and Validation")

    # Conclusions derived from the "03 - Correlation_Study" notebook
    st.success(
        f"**H1 - Property size influences sale price.**\n"
        f"We hypothesize that larger properties tend to have higher sale prices.\n"
        f"* **Validated:** Our correlation study shows that features representing property size have a positive and moderate correlation with sale price.\n\n"

        f"**H2 - Quality impacts value.**\n"
        f"We hypothesize that better quality and condition ratings of a house correspond to higher sale prices.\n"
        f"* **Validated:** The correlation analysis confirms this, particularly through features like kitchen quality and overall quality ratings, which show a strong positive relationship with sale price.\n\n"

        f"**H3 - Age and renovations affect value.**\n"
        f"We hypothesize that a property's age and whether it has undergone recent renovations significantly influence its sale price.\n"
        f"* **Validated:** The correlation study highlights moderate positive relationships between sale price and features such as the year the house was built and whether it had recent renovations."
    )
