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

# Custom function to format numbers with commas and no decimal places
def format_number(number):
    if pd.notna(number) and isinstance(number, (int, float)):
        return '{:,.0f}'.format(number)
    else:
        return 'Laiase with Finance'


# Filtering based on user input
if search_policy:
    policy_results = df[df['Policy Number'].str.contains(search_policy, case=False)]

    if policy_results.empty:
        st.write("Data Not Available")
    else:
        # Replace NaN values in 'Installment' with corresponding 'Claim Amount'
        policy_results['Installment'] = policy_results['Installment'].fillna(policy_results['Claim Amount'])

        # Format 'Claim Amount' and 'Installment' columns with commas and no decimal places
        policy_results['Claim Amount'] = policy_results['Claim Amount'].apply(format_number)
        policy_results['Installment'] = policy_results['Installment'].apply(format_number)

        # Format 'Date Scheduled' column to display full month name
        policy_results['Date Scheduled'] = pd.to_datetime(policy_results['Date Scheduled']).dt.strftime('%B %d, %Y')

        st.table(policy_results[['Insured ', 'Policy Number', 'Claim Type', 'Date Scheduled', 'Claim Amount', 'Installment']])

if search_name:
    name_results = df[df['Insured '].str.contains(search_name, case=False)]

    if name_results.empty:
        st.write("Data Not Available")
    else:
        # Replace NaN values in 'Installment' with corresponding 'Claim Amount'
        name_results['Installment'] = name_results['Installment'].fillna(name_results['Claim Amount'])

        # Format 'Claim Amount' and 'Installment' columns with commas and no decimal places
        name_results['Claim Amount'] = name_results['Claim Amount'].apply(format_number)
        name_results['Installment'] = name_results['Installment'].apply(format_number)

        # Format 'Date Scheduled' column to display full month name
        name_results['Date Scheduled'] = pd.to_datetime(name_results['Date Scheduled']).dt.strftime('%B %d, %Y')

        st.table(name_results[['Insured ', 'Policy Number', 'Claim Type','Date Scheduled', 'Claim Amount', 'Installment']])

