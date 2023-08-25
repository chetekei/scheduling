import streamlit as st
import pandas as pd
import datetime

# configuration
st.set_option('deprecation.showfileUploaderEncoding', False)

# title of the app
st.title("Life Claims Payment Schedule ")

# Add a sidebar
st.sidebar.image('corplogo.PNG', use_column_width=True)
st.sidebar.subheader("Search Clients Details")

# Load the CSV file
csv_file_path = 'scheduled_data.csv'  
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

        styled_results = policy_results[['Insured ', 'Policy Number', 'Claim Type', 'Date Scheduled', 'Claim Amount', 'Installment']].style\
            .set_table_styles([{'selector': 'th',
                                'props': [('background-color', '#f19cbb'),
                                          ('font-weight', 'bold')]}])

        st.table(styled_results)

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

         # Reset the index and remove the default index column
        name_results.reset_index(drop=True, inplace=True)

       # Style the table
        styled_results = name_results[['Insured ', 'Policy Number', 'Claim Type', 'Date Scheduled', 'Claim Amount', 'Installment']].style\
            .set_table_styles([{'selector': 'th',
                                'props': [('background-color', '#f19cbb'),
                                          ('font-weight', 'bold')]}])

        st.table(styled_results)


        
        #st.table(name_results[['Insured ', 'Policy Number', 'Claim Type','Date Scheduled', 'Claim Amount', 'Installment']])

# Convert the 'Date Scheduled' column to datetime
df['Date Scheduled'] = pd.to_datetime(df['Date Scheduled'])

# Get the start date of the current week (Monday)
today = datetime.datetime.today()
start_of_week = today - datetime.timedelta(days=today.weekday())

# Calculate the date for Monday of the current week
monday_of_week = start_of_week + datetime.timedelta(days=0)  # Monday is the first day (0 index)

# Convert 'Date Scheduled' column to dates only
df['Date Scheduled'] = pd.to_datetime(df['Date Scheduled']).dt.date

# Filter the DataFrame for policies rescheduled to be paid on Monday of the current week
policies_scheduled_on_monday = df[df['Date Scheduled'] == monday_of_week.date()]

# Save the filtered DataFrame to a CSV file
policies_scheduled_on_monday.to_csv('policies_scheduled_on_monday.csv', index=False)

# ...

# Add a section for downloading policies scheduled to be paid on Monday
st.sidebar.markdown("### Download Policies Scheduled on Monday")
if st.sidebar.button("Download CSV"):
    # Create a link to download the CSV file
    with open('policies_scheduled_on_monday.csv', 'rb') as f:
        st.sidebar.download_button("Download Policies Scheduled on Monday CSV", f.read(), file_name='policies_scheduled_on_monday.csv')
