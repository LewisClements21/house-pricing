import streamlit as st
def page_summary_body():
    st.write("### Quick Project Summary")
    # text based on README file - "Dataset Content" section
    st.info(
        f"**Project Terms & Jargons**\n\n"
        f"**Project Dataset**\n"
        )
    # Link to README file, so the users can have access to full project documentation
    st.write(
        f"* For additional information, please visit and **read** the "
        f"[Project README file](https://github.com/LewisClements21/house-pricing.git).")
    
    # copied from README file - "Business Requirements" section
    st.success(
        f"The project has 2 business requirements:\n"
        f"* 1 - The client is interested in discovering how house attributes correlate with sale prices."
        f" Therefore, the client expects data visualizations of the correlated variables against the sale price.\n"
        f"* 2 - The client is interested in predicting the house sale prices from her 4 inherited houses,"
        f" and any other house in Ames, Iowa."
        )