# Home.py
import streamlit as st
import pandas as pd
import requests
import numpy as np
import matplotlib.pyplot as plt

def show_home():
    st.title("Credit Application Risk Assessment")

    # --- 1. Load IDs and data from data.csv ---
    df = pd.read_csv("data.csv")  
    id_list = df['SK_ID_CURR'].tolist()

    # Select the 20 columns to display
    columns_to_display = [
        'SK_ID_CURR', 'TARGET', 'CODE_GENDER', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY',
        'CNT_CHILDREN', 'AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY', 
        'AMT_GOODS_PRICE', 'DAYS_BIRTH', 'DAYS_EMPLOYED', 'DAYS_REGISTRATION', 
        'DAYS_ID_PUBLISH', 'REGION_POPULATION_RELATIVE', 'HOUR_APPR_PROCESS_START',
        'OBS_30_CNT_SOCIAL_CIRCLE', 'DEF_30_CNT_SOCIAL_CIRCLE', 'EXT_SOURCE_1', 
        'EXT_SOURCE_2'
    ]

    selected_id = st.selectbox("Select Client ID:", id_list)

    selected_data = df[df['SK_ID_CURR'] == selected_id][columns_to_display]
    selected_data = selected_data.applymap(lambda x: f"{int(x):,}".replace(",", "") if isinstance(x, (int, float)) and not np.isnan(x) else x)
    st.subheader("Client Information")
    st.write(selected_data)

    api_url = "https://mirzayusof.pythonanywhere.com/predict"

    def call_api(api_endpoint, id_value): 
        url = f"{api_endpoint}?param={id_value}"
        response = requests.get(url)
        return response.json()

    api_response = call_api(api_url, selected_id)

    st.subheader("Credit Risk Assessment Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Risk Level",
            value="High Risk" if api_response["prediction"] == 1 else "Low Risk",
            delta="Above Threshold" if api_response["probability"] > api_response["threshold"] else "Below Threshold",
            delta_color="inverse"
        )

    with col2:
        probability_percentage = f"{api_response['probability']*100:.1f}%"
        st.metric(
            label="Default Probability",
            value=probability_percentage,
            delta=f"Threshold: {api_response['threshold']*100:.1f}%"
        )

    with col3:
        st.metric(
            label="Estimated Business Cost",
            value=f"${api_response['business_cost']:,}",
            help="Potential business impact if credit is approved"
        )

    st.info(f"""
    **Assessment Summary:**
    - Client ID: {api_response['SK_ID_CURR']}
    - {'❗ This application is flagged as high risk' if api_response['prediction'] == 1 else '✅ This application is considered low risk'}
    - The probability of default is {probability_percentage} (threshold: {api_response['threshold']*100:.1f}%)
    - Potential business cost: ${api_response['business_cost']:,}
    """)

    st.subheader("Data Analysis")

    x_column = st.selectbox("Select column for X-axis", df.columns)
    y_column = st.selectbox("Select column for Y-axis", df.columns)

    if pd.api.types.is_numeric_dtype(df[x_column]) and pd.api.types.is_numeric_dtype(df[y_column]):
        plt.figure(figsize=(10, 6))
        plt.scatter(df[x_column], df[y_column], color='blue', alpha=0.5, label='Other Clients')
        
        selected_x = df.loc[df['SK_ID_CURR'] == selected_id, x_column].values[0]
        selected_y = df.loc[df['SK_ID_CURR'] == selected_id, y_column].values[0]
        plt.scatter(selected_x, selected_y, color='green' if api_response["prediction"] == 0 else 'red', 
                    s=100, label=f'Selected Client', edgecolor='black', linewidth=2)
        
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.title(f'{x_column} vs {y_column} Analysis')
        plt.legend()
        
        st.pyplot(plt)
    else:
        st.warning("Please select numeric columns for both X and Y axes to generate the plot.")

    # Button to switch to analysis page
    if st.button("View Additional Analysis"):
        st.session_state.page = "analysis"
        st.rerun()
