import streamlit as st
import pandas as pd
import datetime
import base64

# configuration
st.set_option('deprecation.showfileUploaderEncoding', False)

# title of the app
st.title("Life Claims Payment Schedule ")

# Add a sidebar
st.sidebar.image('corplogo.PNG', use_column_width=True)
st.sidebar.subheader("Search Clients Details")

# Load the CSV file
csv_file_path = 'lastshedule.csv'  
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
# Convert 'Policy Number' column to string
df['Policy Number'] = df['Policy Number'].astype(str)

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
        policy_results['Re - scheduled Date'] = pd.to_datetime(policy_results['Re - scheduled Date']).dt.strftime('%B %d, %Y')

        styled_results = policy_results[['Insured ', 'Policy Number', 'Claim Type', 'Date Scheduled', 'Re - scheduled Date', 'Claim Amount', 'Payment']].style\
            .set_table_styles([{'selector': 'th',
                                'props': [('background-color', '#f19cbb'),
                                          ('font-weight', 'bold')]}])

        st.table(styled_results)

if search_name:
    name_results = df[df['Insured '].str.contains(search_name, case=False)]

    if name_results.empty:
        st.write("Data Not Available")
    else:
        
        # Format 'Claim Amount' and 'Installment' columns with commas and no decimal places
        name_results['Claim Amount'] = name_results['Claim Amount'].apply(format_number)
        name_results['Installment'] = name_results['Installment'].apply(format_number)

        
        name_results['Date Scheduled'] = pd.to_datetime(name_results['Date Scheduled']).dt.strftime('%B %d, %Y')
        name_results['Re - scheduled Date'] = pd.to_datetime(name_results['Re - scheduled Date']).dt.strftime('%B %d, %Y')

         # Reset the index and remove the default index column
        name_results.reset_index(drop=True, inplace=True)

       # Style the table
        styled_results = name_results[['Insured ', 'Policy Number', 'Claim Type', 'Date Scheduled', 'Re - scheduled Date', 'Claim Amount', 'Payment']].style\
            .set_table_styles([{'selector': 'th',
                                'props': [('background-color', '#f19cbb'),
                                          ('font-weight', 'bold')]}])

        st.table(styled_results)

# Add a section to download policies scheduled for the respective week in the sidebar
st.sidebar.markdown("---")

def get_download_link(data_frame):
    csv = data_frame.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="policies_this_week.csv">Click here to download the CSV file</a>'
    return href

# ... (filtering and formatting code)

if st.sidebar.button("Scheduled Payments for This Week"):
    # Assuming your 'Date Scheduled' column contains the date information
    current_date = datetime.datetime.now()
    start_of_week = current_date - datetime.timedelta(days=current_date.weekday())
    end_of_week = start_of_week + datetime.timedelta(days=6)
    
    policies_this_week = df[(pd.to_datetime(df['Re - scheduled Date']).dt.date >= start_of_week.date()) & (pd.to_datetime(df['Re - scheduled Date']).dt.date <= end_of_week.date())]
    
    columns_to_include = ['Claim Type', 'Insured ', 'Policy Number', 'Sum Assured', 'Claim Amount', 'Re - scheduled Date']
    policies_selected_columns = policies_this_week[columns_to_include]

    # Calculate the total Claim Amount
    total_claim_amount = policies_selected_columns['Claim Amount'].sum()
    

    st.subheader("Payments Scheduled for This Week")
    formatted_total_claim_amount = '{:,.0f}'.format(total_claim_amount)
    st.write(f" **Total Scheduled Claim Amount this Week:** {formatted_total_claim_amount}")
    
    st.dataframe(policies_selected_columns)

    

    
    # Provide the download link in the sidebar
    st.sidebar.markdown(get_download_link(policies_selected_columns), unsafe_allow_html=True)
