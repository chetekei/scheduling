import streamlit as st
import pandas as pd
import gspread
from google.oauth2 import service_account
import base64
import datetime


def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("User not known or incorrect password")
        return False
    else:
        # Password correct.
        return True

if check_password():

    # Define your Google Sheets credentials JSON file (replace with your own)
    credentials_path = 'corplife-c1a7f61f3ef5.json'
        
    # Authenticate with Google Sheets using the credentials
    credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=['https://spreadsheets.google.com/feeds'])
        
    # Authenticate with Google Sheets using gspread
    gc = gspread.authorize(credentials)
        
    # Your Google Sheets URL
    url = "https://docs.google.com/spreadsheets/d/15cLyNuhQ5f-HuhmUku7aoaEKLe6oO1tUHQSe0EgypQA/edit#gid=0"
        
    # Open the Google Sheets spreadsheet
    worksheet = gc.open_by_url(url).worksheet("payments")


    # Configuration
    st.set_option('deprecation.showfileUploaderEncoding', False)

    # Add a sidebar
    st.sidebar.image('corplogo.PNG', use_column_width=True)
    st.sidebar.subheader("Search Clients Details")  # User input for plan selection

    # Create a sidebar to switch between views
    view = st.sidebar.radio("View", ["Scheduling", "Payments", "Calculate Surrender"])

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
                name = st.text_input("Enter name of the insured")
                policy_number = st.text_input("Enter Policy Number")
                sum_assured = int(st.number_input("Enter the Sum Assured:"))
                units_paid = int(st.number_input("Enter the number of units Paid"))
                policy_term = int(st.number_input("Enter the Policy Term"))
                prepared = st.selectbox("Prepared By:",['Mary', 'Lennox'])
                

                # "Calculate" button
                if st.button("Calculate"):
                    # Function to retrieve the adjusted value at the intersection of a selected column and TERM
                    def get_adjusted_value(data_frame, units_paid, policy_term, sum_assured):
                        try:
                            row_index = data_frame[data_frame['TERM'] == policy_term].index[0]
                            column_name = str(units_paid)  # Convert units_paid to string for column name
                            value = data_frame.at[row_index, column_name]  # Access the cell using .at method

                            adjusted_value = float(value) / 1000 * sum_assured
                            return adjusted_value
                        
                        except (KeyError, IndexError):
                            return "Invalid column name or TERM value."

                

                    # Calculate the adjusted value if all user inputs are provided
                    # Calculate the adjusted value if all user inputs are provided
                    adjusted_value = get_adjusted_value(df, units_paid, policy_term, sum_assured)
                    
                    if isinstance(adjusted_value, (int, float)):
                        row_index = df[df['TERM'] == policy_term].index[0]
                        column_name = str(units_paid)
                        value = df.at[row_index, column_name]
                        formatted_value = (value/1000)                  
                        
                    
                        st.write(f"The Surrender Value is: <br> (*{formatted_value}*)  *  {sum_assured:,} <br> =  **{adjusted_value:,.0f}**" , unsafe_allow_html=True)

                        url = "https://www.bing.com/images/search?view=detailV2&ccid=vKHeGPlO&id=D2CE01A41EF4AF363F21CABE144E3BDD731650D1&thid=OIP.vKHeGPlOz4iZMsq0QMQH0wHaDD&mediaurl=https%3A%2F%2Fsokodirectory.com%2Fwp-content%2Fuploads%2F2016%2F07%2FCorporate-Insurance-Company.jpg&cdnurl=https%3A%2F%2Fth.bing.com%2Fth%2Fid%2FR.bca1de18f94ecf889932cab440c407d3%3Frik%3D0VAWc907ThS%252byg%26pid%3DImgRaw%26r%3D0&exph=290&expw=702&q=corporate+insurance+company&simid=607988656116206866&form=IRPRST&ck=61276C047C84B7600CC7E0B7DCE160A4&selectedindex=1&ajaxhist=0&ajaxserp=0&pivotparams=insightsToken%3Dccid_yEaMgL9j*cp_D100553B4A8B4CD3E464B2AC98388A56*mid_683292741C7A6890D8DA31F255E89A2F34245170*simid_608003598316414949*thid_OIP.yEaMgL9jGkcRS9gptq4r8gAAAA&vt=0&sim=11&iss=VSI&ajaxhist=0&ajaxserp=0"

                        # Create an HTML report
                        html_report = f"""
                        <html>
                        <head>
                            <style>
                                body {{ font-family: Arial, sans-serif; }}
                                h1 {{ color: black; }}
                            </style>
                        </head>
                        <body style="text-align: center;">
                            <img src="https://viva-365.com/wp-content/uploads/2021/01/Corporate-Insurance.png" alt="Your Image" width="150">
                            <h2> SURRENDER VALUE</h2>
                            <p><strong>Insured:</strong> {name}</p>
                            <p><strong>Policy Number:</strong> {policy_number}</p>
                            <p><strong>Sum Assured:</strong> {sum_assured:,.0f}</p>
                            <p><strong>Policy Term:</strong> {policy_term}</p>
                            <p><strong>Units Paid:</strong> {units_paid}</p><br>                        
                            <p><strong>Surrender Value:</strong> ({formatted_value})  *  ({sum_assured:,})  = <strong>Ksh. {adjusted_value:,.0f}</strong</p>
                            <p style="position: absolute; bottom: 0;"><strong>Prepared By:</strong>{prepared}</p>
                        </body>
                        </html>
                        """
                        
                    # Create a download button with customized file name
                
                        st.download_button(
                            label=f"Download {name}'s surrender value (HTML)",
                            data=html_report.encode('utf-8'),
                            file_name=f"{name}_score_report.html",
                            mime="text/html"
                        )


                    else:
                        st.write(adjusted_value)
                    
            else:
                st.write("Invalid plan selection. Please enter a valid plan number.")


    elif view == 'Payments':

        st.subheader("LIFE PAYMENTS")
        
        # Read data from the Google Sheets worksheet
        data = worksheet.get_all_values()
        headers = data[0]
        data = data[1:]

        df = pd.DataFrame(data, columns = headers)

        
        # Get the unique reviewer names from the DataFrame
        unique_month = df['Month Paid'].unique()

        # Create a dropdown to select a month with "All Payments" option
        selected = st.selectbox("Filter by Month Payment Done:", ["All Payments"] + list(unique_month))

        if selected != "All Payments":
            # Filter the DataFrame based on the selected month
            filtered_df = df[df['Month Paid'] == selected]
        else:
            # If "All Payments" is selected, show the entire DataFrame
            filtered_df = df

      
        
        st.dataframe(filtered_df)

        filtered_df['Amount'] = pd.to_numeric(filtered_df['Amount'], errors='coerce')

        total = filtered_df['Amount'].sum()
        
        st.markdown (f"Total Amount Paid in **{selected}**: **{total}**")
        


    elif view == "Scheduling":
        
        st.title("Life Claims Payment Schedule")
        csv_file_path = 'final.csv'  
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
                policy_results['Payment'] = policy_results['Payment'].apply(format_number)

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
                name_results['Payment'] = name_results['Payment'].apply(format_number)

                
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
