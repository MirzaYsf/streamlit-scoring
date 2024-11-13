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
    st.title("Distribution Analysis")

    # Load data
    df = pd.read_csv("data.csv")

    # Selecting numerical columns for analysis
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    
    # Create centered layout
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Select column to analyze
        selected_column = st.selectbox(
            "Select a feature to analyze:",
            numerical_cols
        )
        
        # Create histogram with enhanced styling
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Plot histogram with more aesthetically pleasing parameters
        plt.hist(df[selected_column].dropna(), 
                bins=30, 
                edgecolor='black',
                color='skyblue',
                alpha=0.7)
        
        # Add mean and median lines
        plt.axvline(df[selected_column].mean(), 
                   color='red', 
                   linestyle='dashed', 
                   linewidth=1,
                   label=f'Mean: {df[selected_column].mean():.2f}')
        plt.axvline(df[selected_column].median(), 
                   color='green', 
                   linestyle='dashed', 
                   linewidth=1,
                   label=f'Median: {df[selected_column].median():.2f}')
        
        # Enhance the plot appearance
        plt.title(f'Distribution of {selected_column}', pad=20)
        plt.xlabel(selected_column)
        plt.ylabel('Frequency')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Display plot
        st.pyplot(fig)
        
        # Display summary statistics in a clean format
        st.subheader("Summary Statistics")
        
        # Calculate statistics
        stats = {
            "Count": len(df[selected_column].dropna()),
            "Mean": df[selected_column].mean(),
            "Median": df[selected_column].median(),
            "Std Dev": df[selected_column].std(),
            "Min": df[selected_column].min(),
            "Max": df[selected_column].max(),
            "Null Values": df[selected_column].isnull().sum()
        }
        
        # Create two columns for statistics
        stat_col1, stat_col2 = st.columns(2)
        
        with stat_col1:
            st.markdown("**Basic Statistics:**")
            st.write(f"• Count: {stats['Count']:,.0f}")
            st.write(f"• Mean: {stats['Mean']:,.2f}")
            st.write(f"• Median: {stats['Median']:,.2f}")
            st.write(f"• Std Dev: {stats['Std Dev']:,.2f}")
            
        with stat_col2:
            st.markdown("**Range Information:**")
            st.write(f"• Minimum: {stats['Min']:,.2f}")
            st.write(f"• Maximum: {stats['Max']:,.2f}")
            st.write(f"• Range: {stats['Max']-stats['Min']:,.2f}")
            st.write(f"• Missing Values: {stats['Null Values']:,}")

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
