import streamlit as st

def page_summary_body():
    """
    Displays contents of the project summary page
    """
    st.write("### Quick Project Summary")

    st.info(
        f"**Project Terms & Jargons**\n\n"
        f"* **Sales price** of a house refers to the current market price, in US dollars,\
         of a house with with various attributes.\n"
        f"* **Inherited house** is a house that the client inherited from grandparents.\n"
        f"* **Summed price** is the total of the predicted sales prices of the four inherited houses.\n\n"
        )
    
     # text based on README file - "Dataset Content" section
    st.info(
        f"**Project Dataset**\n"
        f"* The project dataset comes from housing price database from Ames, Iowa.\
         It is available in [Kaggle via Code Institute](https://www.kaggle.com/codeinstitute/housing-prices-data),\
         and includes sales price (the target) and features that show a house's age (year built, year remodeled),\
         property size (e.g., first floor area, second floor area, garaze area) and quality assessments."
        )

    # Link to README file, so the users can have access to full project documentation
    st.write(
        f"* For additional information, please visit and **read** the "
        f"[Project README file](https://github.com/Amareteklay/heritage-housing-issues).")
    

    # copied from README file - "Business Requirements" section
    st.success(
        f"**Project Business Requirements**\n\n"
    
        f"The project has 2 business requirements:\n"
        f"* **BR1** - The client is interested in discovering how house attributes correlate with sale prices."
        f" Therefore, the client expects data visualizations of the correlated variables against the sale price.\n\n"
        f"* **BR2** - The client is interested in predicting the house sale prices from her 4 inherited houses,"
        f" and any other house in Ames, Iowa."
        )

        