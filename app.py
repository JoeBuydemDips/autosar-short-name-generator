import streamlit as st
import pandas as pd
from utils import *

# Streamlit UI
st.title('Autosar Parameter Name Toolbox 🧰')

# Define the list of options
options = ["Generate Short Name", "Find Long Name"]

# create radio buttons with Generate Short name as default
selected_option = st.radio("Select Your Option 📋", options, index=0)

# read dataframe
df = pd.read_csv("autosar_data.csv")

# Side Bar
st.sidebar.title("Searchable Autosar Parameter Keyword List")
st.sidebar.dataframe(df, hide_index=True, use_container_width=True)

# ---------------------------------------------------------------------------------------------------
# Section For Short Name Generator
# ---------------------------------------------------------------------------------------------------
if selected_option == "Generate Short Name":

    short_name_options = ["Single", "Multiple"]
    short_name_selected_option = st.radio("Single or Multiple Parameters 😜", short_name_options, index=0)

    # Single User Input
    if short_name_selected_option == "Single": 
        # User input
        user_input = st.text_input("Parameter Long Name", placeholder='Enter long name: eg. Accelerator Pedal')

        if st.button("Generate Short Name"):
            if user_input:
                # st.subheader("Parameter Short Name")
                # st.write(long_name_to_short_name(user_input, df))
                short_name, valid = long_name_to_short_name(user_input, df)
                # st.text_area("Parameter Short Name", short_name, disabled=True)
                st.subheader("Parameter Short Name")
                if valid:
                    st.success(short_name, icon="✅")
                else:
                    st.warning(short_name, icon="⚠️")

    # Multiple User Input
    else:
        user_input = st.text_area("Parameter Long Names", placeholder='Enter a list of long names on each line: eg. Accelerator Pedal', height=250)

         # column data for the table
        column_data = {
            'Long Name': [],
            'Short Name': []
        }

        if st.button("Generate Short Names"):
            if user_input:
                input_list = user_input.split('\n')
                # Filter out any empty strings if there are empty lines
                input_list = [line for line in input_list if line.strip() != '']

                # Example loop that populates the column data
                for input in input_list: 
                    # Generate data for each column
                    short_name, valid = long_name_to_short_name(input, df)
                    data_for_column_1 = f'{input}'  # Replace with your actual data generation logic
                    data_for_column_2 = f'{short_name}'  # Replace with your actual data generation logic
                    
                    # Append the data to the respective lists
                    column_data['Long Name'].append(data_for_column_1)
                    column_data['Short Name'].append(data_for_column_2)

                # Convert the column data to a pandas DataFrame
                table_df = pd.DataFrame(column_data)
                # table_df_reset = table_df.reset_index(drop=True)


                # Display the DataFrame as a table in Streamlit
                # st.table(table_df_reset)
                st.dataframe(table_df, hide_index=True, use_container_width=True)

# ---------------------------------------------------------------------------------------------------
# Section For Long Name Finder
# ---------------------------------------------------------------------------------------------------
elif selected_option == "Find Long Name":

    long_name_options = ["Single", "Multiple"]
    long_name_selected_option = st.radio("Single or Multiple Parameters 😜", long_name_options, index=0)

    # Single User Input
    if long_name_selected_option == "Single": 

        # User input
        user_input = st.text_input("Parameter Short Name", placeholder='Enter short name: eg. AccrPedl')

        if st.button("Generate Long Name"):
            if user_input:
                
                # st.write(long_name_to_short_name(user_input, df))
                long_name, valid = short_name_to_long_name(user_input, df)
                # st.text_area("Parameter Long Name", long_name, disabled=True)
                st.subheader("Parameter Long Name")
                if valid:
                    st.success(long_name, icon="✅")
                else:
                    st.warning(long_name, icon="⚠️")

    # Multiple User Input
    else:
        user_input = st.text_area("Parameter Short Names", placeholder='Enter a list of short names on each line: eg. AccrPedl', height=250)

         # column data for the table
        column_data = {
            'Short Name': [],
            'Long Name': []
        }

        if st.button("Generate Long Names"):
            if user_input:
                input_list = user_input.split('\n')
                # Filter out any empty strings if there are empty lines
                input_list = [line for line in input_list if line.strip() != '']

                # Example loop that populates the column data
                for input in input_list: 
                    # Generate data for each column
                    short_name, valid = short_name_to_long_name(input, df)
                    data_for_column_1 = f'{input}'  # Replace with your actual data generation logic
                    data_for_column_2 = f'{short_name}'  # Replace with your actual data generation logic
                    
                    # Append the data to the respective lists
                    column_data['Short Name'].append(data_for_column_1)
                    column_data['Long Name'].append(data_for_column_2)

                # Convert the column data to a pandas DataFrame
                table_df = pd.DataFrame(column_data)
                # table_df_reset = table_df.reset_index(drop=True)


                # Display the DataFrame as a table in Streamlit
                # st.table(table_df_reset)
                st.dataframe(table_df, hide_index=True, use_container_width=True)