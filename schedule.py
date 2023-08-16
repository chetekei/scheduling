import streamlit as st
import pandas as pd

# configuration
st.set_option('deprecation.showfileUploaderEncoding', False)

# title of the app
st.title("Life Claims Payment Schedule ")

# Add a sidebar
st.sidebar.image('corplogo.PNG', use_column_width=True)
st.sidebar.subheader("Search Clients Details")

# Load the CSV file
csv_file_path = 'finalclientdata.csv'  
df = pd.read_csv(csv_file_path)

# Sidebar input boxes
search_policy = st.sidebar.text_input("Search by Policy Number", "")
search_name = st.sidebar.text_input("Search by Client Name", "")

# Filtering based on user input
if search_policy:
    policy_results = df[df['Policy Number'].str.contains(search_policy, case=False)]
    
    st.table(policy_results[['Insured ', 'Policy Number', 'Claim Type', 'Maturity Year', 'Date Scheduled', 'Claim Amount', 'Installment']])

if search_name:
    name_results = df[df['Insured '].str.contains(search_name, case=False)]
    
    st.table(name_results[['Insured ', 'Policy Number', 'Claim Type', 'Maturity Year', 'Date Scheduled', 'Claim Amount', 'Installment']])
