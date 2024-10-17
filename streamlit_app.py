import streamlit as st
import pandas as pd
import requests
import numpy as np
import matplotlib.pyplot as plt

# --- 1. Load IDs and data from data.csv ---
df = pd.read_csv("data.csv")  
id_list = df['SK_ID_CURR'].tolist()  # List of IDs

# Select the 20 columns to display
columns_to_display = [
    'SK_ID_CURR', 'TARGET', 'CODE_GENDER', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY',
    'CNT_CHILDREN', 'AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY', 
    'AMT_GOODS_PRICE', 'DAYS_BIRTH', 'DAYS_EMPLOYED', 'DAYS_REGISTRATION', 
    'DAYS_ID_PUBLISH', 'REGION_POPULATION_RELATIVE', 'HOUR_APPR_PROCESS_START',
    'OBS_30_CNT_SOCIAL_CIRCLE', 'DEF_30_CNT_SOCIAL_CIRCLE', 'EXT_SOURCE_1', 
    'EXT_SOURCE_2'
]

# --- 2. Create the Streamlit app ---
st.title("Scoring")

# Dropdown to select SK_ID_CURR
selected_id = st.selectbox("Select an ID:", id_list)  # Dropdown list

# --- 3. Automatically display selected ID data ---
# Find the data for the selected ID and format it to remove commas
selected_data = df[df['SK_ID_CURR'] == selected_id][columns_to_display]

# Apply formatting to remove commas from numbers, while handling NaN values
selected_data = selected_data.applymap(lambda x: f"{int(x):,}".replace(",", "") if isinstance(x, (int, float)) and not np.isnan(x) else x)

# Display the relevant columns for the selected ID
st.write(selected_data)

# --- 4. Define and call the API ---
api_url = "https://mirzayusof.pythonanywhere.com/predict"  # API URL

def call_api(api_endpoint, id_value): 
    url = f"{api_endpoint}?param={id_value}"
    response = requests.get(url)
    return response.json()  

# Automatically call the API when an ID is selected and display the response
api_response = call_api(api_url, selected_id)
st.write("API Response:", api_response)

# --- 5. Add graph selection options ---
st.subheader("Plot the Data")

# Select columns for X and Y axes
x_column = st.selectbox("Select column for X-axis", df.columns)
y_column = st.selectbox("Select column for Y-axis", df.columns)

# Check if the selected columns are numeric (to avoid errors in plotting)
if pd.api.types.is_numeric_dtype(df[x_column]) and pd.api.types.is_numeric_dtype(df[y_column]):

    # --- 6. Create the 2D scatter plot ---
    plt.figure(figsize=(10, 6))

    # Plot all points in blue
    plt.scatter(df[x_column], df[y_column], color='blue', label='Other IDs')

    # Highlight the selected ID in green with larger size and bold style
    selected_x = df.loc[df['SK_ID_CURR'] == selected_id, x_column].values[0]
    selected_y = df.loc[df['SK_ID_CURR'] == selected_id, y_column].values[0]
    plt.scatter(selected_x, selected_y, color='green', s=100, label=f'Selected ID: {selected_id}', edgecolor='black', linewidth=2)

    # Add labels and title to the plot
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f'{x_column} vs {y_column} Scatter Plot')

    # Show legend
    plt.legend()

    # Display the plot
    st.pyplot(plt)
else:
    st.write("Please select numeric columns for both X and Y axes to plot.")

