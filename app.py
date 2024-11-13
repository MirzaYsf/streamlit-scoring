# app.py
import streamlit as st
from PIL import Image
import os
from Home import show_home

# Configuration initiale
st.set_page_config(
    page_title="Credit Risk Dashboard",
    page_icon="💰",
    layout="wide"
)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = "home"

# Function to show image analysis page
def show_image_analysis():
    st.title("Model Analysis & Documentation")

    # Création de deux colonnes pour les images
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Dashboard Schema")
        try:
            dashboard_image = Image.open("dashboard_schema.jpg")
            st.image(dashboard_image, 
                    caption="Dashboard Architecture Schema",
                    use_column_width=True)
            
            st.markdown("""
            **Description for screen readers:**
            This image shows the architectural schema of our dashboard,
            illustrating the flow of data from the client request through
            our risk assessment model to the final visualization.
            """)
        except:
            st.error("Dashboard schema image not found. Please ensure 'dashboard_schema.jpg' is in the same folder.")

    with col2:
        st.subheader("Model Performance")
        try:
            performance_image = Image.open("model_performance.jpg")
            st.image(performance_image,
                    caption="Model Performance Metrics",
                    use_column_width=True)
            
            st.markdown("""
            **Description for screen readers:**
            This image displays the performance metrics of our credit risk model,
            including confusion matrix, ROC curve, and key performance indicators.
            """)
        except:
            st.error("Model performance image not found. Please ensure 'model_performance.jpg' is in the same folder.")

    st.markdown("---")
    st.subheader("Additional Information")
    st.markdown("""
    This page provides visual documentation of our credit risk assessment system:
    - The **Dashboard Schema** illustrates how different components of our system interact
    - The **Model Performance** metrics show how well our model performs in predicting credit risk

    For more detailed information, please refer to the technical documentation or contact the data science team.
    """)

    # Button to return to home
    if st.button("Return to Dashboard"):
        st.session_state.page = "home"
        st.experimental_rerun()

# Main App Logic
def main():
    if st.session_state.page == "home":
        show_home()
    else:
        show_image_analysis()

if __name__ == "__main__":
    main()
