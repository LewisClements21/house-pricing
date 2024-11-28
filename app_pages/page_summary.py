import streamlit as st

def page_summary_body():
    """
    Displays the contents of the project summary page
    """
    st.write("### Quick Project Summary")

    # Definitions of project-specific terms and concepts
    st.info(
        f"**Project Terms & Definitions**\n\n"
        f"* **Sale price:** The current market value (in US dollars) of a house, determined by various attributes.\n"
        f"* **Inherited house:** A property the client has inherited from their grandparents.\n"
        f"* **Summed price:** The total predicted sales value of the four inherited houses.\n"
    )

    # Dataset description based on the README file
    st.info(
        f"**Project Dataset**\n\n"
        f"The dataset used in this project originates from the Ames, Iowa housing price database. "
        f"It is accessible via [Kaggle through Code Institute](https://www.kaggle.com/codeinstitute/housing-prices-data). "
        f"The dataset includes the target variable (sale price) and features such as a house's age "
        f"(e.g., year built, year remodeled), property size (e.g., first and second-floor areas, garage area), "
        f"and quality assessments."
    )

    # Link to the README file for detailed documentation
    st.write(
        f"* For more detailed information, refer to the "
        f"[Project README file](https://github.com/LewisClements21/house-pricing/blob/main/README.md)."
    )

    # Business requirements summary copied from the README file
    st.success(
        f"**Project Business Requirements**\n\n"
        f"The project is designed to meet two primary business requirements:\n\n"
        f"* **BR1:** The client aims to understand how various house attributes correlate with sale prices. "
        f"As such, they expect data visualizations illustrating these correlations.\n\n"
        f"* **BR2:** The client seeks to predict the sale prices of her four inherited houses "
        f"and any other properties in Ames, Iowa."
    )
