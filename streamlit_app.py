# app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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

def show_analysis():
    st.title("Additional Analysis")

    # Load data
    df = pd.read_csv("data.csv")

    # Selecting numerical columns for analysis
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    
    # Create two columns for the layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribution Analysis")
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
        summary_stats = df[selected_column].describe()
        st.write(summary_stats)
        
        st.markdown(f"""
        **Quick insights for {selected_column}:**
        - Number of null values: {df[selected_column].isnull().sum()}
        - Skewness: {df[selected_column].skew():.2f}
        - Kurtosis: {df[selected_column].kurtosis():.2f}
        """)

    # Adding correlation analysis
    st.markdown("---")
    st.subheader("Correlation Analysis")
    
    # Select only numeric columns for correlation
    numeric_df = df.select_dtypes(include=[np.number])
    corr_matrix = numeric_df.corr()
    
    # Using seaborn for better correlation heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(corr_matrix, 
                cmap='coolwarm', 
                center=0,
                annot=True,  # Show correlation values
                fmt='.2f',   # Format to 2 decimal places
                square=True,
                cbar_kws={'label': 'Correlation Coefficient'})
    plt.title("Correlation Matrix Heatmap")
    st.pyplot(plt)

    # Adding feature selection based on correlation
    st.subheader("Top Correlations")
    target_correlations = corr_matrix['TARGET'].sort_values(ascending=False)
    st.write("Features most correlated with TARGET:")
    st.write(target_correlations)

    # Button to return to home
    st.markdown("---")
    if st.button("Return to Dashboard"):
        st.session_state.page = "home"
        st.rerun()

# Main App Logic
def main():
    if st.session_state.page == "home":
        show_home()
    else:
        show_analysis()

if __name__ == "__main__":
    main()
