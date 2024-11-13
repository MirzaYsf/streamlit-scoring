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
    
    # Create correlation heatmap using matplotlib
    fig, ax = plt.subplots(figsize=(12, 8))
    im = ax.imshow(corr_matrix, cmap='coolwarm', aspect='auto')
    
    # Add colorbar
    plt.colorbar(im, label='Correlation Coefficient')
    
    # Add labels
    ax.set_xticks(np.arange(len(corr_matrix.columns)))
    ax.set_yticks(np.arange(len(corr_matrix.columns)))
    ax.set_xticklabels(corr_matrix.columns, rotation=90)
    ax.set_yticklabels(corr_matrix.columns)
    
    # Add correlation values
    for i in range(len(corr_matrix.columns)):
        for j in range(len(corr_matrix.columns)):
            text = ax.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                         ha="center", va="center", color="black")
    
    plt.title("Correlation Matrix Heatmap")
    plt.tight_layout()
    st.pyplot(fig)

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
