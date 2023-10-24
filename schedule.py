import streamlit as st
import pandas as pd
import datetime
import base64

# Configuration
st.set_option('deprecation.showfileUploaderEncoding', False)

# Title of the app
st.title("Life Claims Payment Schedule")

# Add a sidebar
st.sidebar.image('corplogo.PNG', use_column_width=True)
st.sidebar.subheader("Search Clients Details")  # User input for plan selection

 # Create a sidebar to switch between views
view = st.sidebar.radio("View", ["Scheduling", "Calculate Surrender"])

if view == "Calculate Surrender":

    plan_selection = st.sidebar.text_input("Enter Plan Code (04, 05, 06, 07, 10 or 20): ")

    # Create a mapping of plan selection to CSV file
    plan_to_csv_mapping = {
        "04": "plan04.csv",
        "05": "plan05.csv",
        "06": "plan06.csv",
        "07": "plan07.csv",
        "10": "plan20.csv",
        "20": "plan20.csv"
    }

    if plan_selection:
        if plan_selection in plan_to_csv_mapping:
            selected_csv_file = plan_to_csv_mapping[plan_selection]
            df = pd.read_csv(selected_csv_file)
            df.columns = df.columns.astype(str)

            # User input for policy details
            units_paid = int(st.number_input("Enter the number of units Paid"))
            policy_term = int(st.number_input("Enter the Policy Term"))
            sum_assured = int(st.number_input("Enter the Sum Assured:"))

            # "Calculate" button
            if st.button("Calculate"):
                # Function to retrieve the adjusted value at the intersection of a selected column and TERM
                def get_adjusted_value(data_frame, units_paid, policy_term, sum_assured):
                    try:
                        row_index = data_frame[data_frame['TERM'] == policy_term].index[0]
                        column_name = str(units_paid)  # Convert units_paid to string for column name
                        value = data_frame.at[row_index, column_name]  # Access the cell using .at method

                        adjusted_value = (value / 1000) * sum_assured
                        return adjusted_value
                    except (KeyError, IndexError):
                        return "Invalid column name or TERM value."

                # Calculate the adjusted value if all user inputs are provided
                if units_paid and policy_term and sum_assured:
                    adjusted_value = get_adjusted_value(df, units_paid, policy_term, sum_assured)
                    if isinstance(adjusted_value, (int, float)):
                        st.write(f"The Surrender Value is: {value/1000 * sum_assured} = {adjusted_value:.2f}")

                    else:
                        st.write(adjusted_value)
        else:
            st.write("Invalid plan selection. Please enter a valid plan number.")

elif view == "Scheduling":
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

            # Format Claim Amount and Installment columns with commas and no decimal places
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
