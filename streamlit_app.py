# app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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

# Function to show analysis page
def show_analysis():
    st.title("Additional Analysis")

    # Load data
    df = pd.read_csv("data.csv")

    # Add some interesting analysis here
    st.subheader("Statistical Overview")
    
    # Selecting numerical columns for analysis
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    
    # Create two columns for the layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribution Analysis")
        # Let user select a column to analyze
        selected_column = st.selectbox(
            "Select a column to analyze:",
            numerical_cols
        )
        
        # Create histogram
        fig, ax = plt.subplots(figsize=(10, 6))
        plt.hist(df[selected_column].dropna(), bins=30, edgecolor='black')
        plt.title(f'Distribution of {selected_column}')
        plt.xlabel(selected_column)
        plt.ylabel('Count')
        st.pyplot(fig)

    with col2:
        st.subheader("Summary Statistics")
        # Display summary statistics for selected column
        summary_stats = df[selected_column].describe()
        st.write(summary_stats)
        
        # Add some additional insights
        st.markdown(f"""
        **Quick insights for {selected_column}:**
        - Number of null values: {df[selected_column].isnull().sum()}
        - Skewness: {df[selected_column].skew():.2f}
        - Kurtosis: {df[selected_column].kurtosis():.2f}
        """)

    # Add correlation heatmap
    st.subheader("Correlation Analysis")
    # Select only numeric columns
    numeric_df = df.select_dtypes(include=[np.number])
    # Calculate correlation matrix
    corr_matrix = numeric_df.corr()
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=(12, 8))
    plt.imshow(corr_matrix, cmap='coolwarm', aspect='auto')
    plt.colorbar()
    plt.xticks(range(len(corr_matrix.columns)), corr_matrix.columns, rotation=90)
    plt.yticks(range(len(corr_matrix.columns)), corr_matrix.columns)
    plt.title("Correlation Matrix Heatmap")
    st.pyplot(fig)

    # Button to return to home
    if st.button("Return to Dashboard"):
        st.session_state.page = "home"
        st.experimental_rerun()

# Main App Logic
def main():
    if st.session_state.page == "home":
        show_home()
    else:
        show_analysis()

if __name__ == "__main__":
    main()
