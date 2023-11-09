import streamlit as st
from utils import *

# Streamlit UI
st.title('Autosar Parameter Short Name Generator And Long Name Finder')

# Define the list of options
options = ["Generate Short Name", "Find Long Name"]

# create radio buttons with Generate Short name as default
selected_option = st.radio("Select Your Option 📋", options, index=0)

# read dataframe
df = pd.read_csv("autosar_data.csv")

if selected_option == "Generate Short Name":
    # User input
    user_input = st.text_input("Parameter Long Name", placeholder='Enter long name: eg. Accelerator Pedal')

    if user_input:
        # st.subheader("Parameter Short Name")
        # st.write(long_name_to_short_name(user_input, df))
        short_name, valid = long_name_to_short_name(user_input, df)
        # st.text_area("Parameter Short Name", short_name, disabled=True)
        st.subheader("Parameter Short Name")
        if valid:
            st.success(short_name)
        else:
            st.warning(short_name)

elif selected_option == "Find Long Name":
    # User input
    user_input = st.text_input("Parameter Short Name", placeholder='Enter short name: eg. AccrPedl')

    if user_input:
        
        # st.write(long_name_to_short_name(user_input, df))
        long_name, valid = short_name_to_long_name(user_input, df)
        # st.text_area("Parameter Long Name", long_name, disabled=True)
        st.subheader("Parameter Long Name")
        if valid:
            st.success(long_name)
        else:
            st.warning(long_name)