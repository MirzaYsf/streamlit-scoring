# Credit Scoring Dashboard for Prêt à dépenser

## Project Overview

This project simulates a professional mission as a Data Scientist for a financial company, **Prêt à dépenser**, which provides consumer credit to individuals with little or no credit history. 

The goal is to develop a **credit scoring dashboard** that allows client relationship managers to explain credit decisions transparently to customers. This tool will enhance communication between the company and its clients and align with the company’s values of transparency.

The dashboard integrates an existing API to compute the credit score and classify the loan as either approved or rejected. The objective is to visualize these decisions and make them comprehensible for non-experts, with accessibility considerations for users with disabilities.

## Features

1. **Credit Score Visualization**:
   - Display the customer's credit score along with the probability of approval (e.g., how close the score is to the approval threshold).
   - Provide an intelligible interpretation of the score.

2. **Customer Profile Overview**:
   - Show key descriptive information about a customer.
   - Compare a customer’s profile with that of all customers or a group of similar customers.

3. **Interactive Visualizations**:
   - Include graphical comparisons between a customer and other clients, based on important variables.
   - Enable filtering through dropdown menus or similar components for comparing specific variables.
   
4. **Accessibility**:
   - Design charts and visual elements following the **WCAG** accessibility guidelines to accommodate users with disabilities.

5. **Cloud Deployment**:
   - The dashboard is deployed on a Cloud platform, making it accessible from different workstations.

6. **Optional**:
   - Allow real-time score updates after modifying one or more customer details.
   - Enable users to input a new customer's profile to generate a credit score and probability prediction.

## Tools and Libraries

- **Streamlit** for developing the interactive dashboard.
- **Python** for backend logic and API interaction.
- **Dash** or **Bokeh** can also be explored for building interactive charts.
- **Matplotlib**/**Plotly** for generating visualizations.
- **Flask API** for handling prediction requests (previously implemented).

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/MirzaYsf/streamlit-scoring.git
   cd streamlit-scoring
