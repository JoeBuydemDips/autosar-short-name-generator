import streamlit as st
from utils import *

# Streamlit UI
st.title('Autosar Parameter Short Name Generator')

# User input
user_input = st.text_input("Parameter Long Name", placeholder='Enter long name: eg. Accelerator Pedal')
df = pd.read_csv("autosar_data.csv")

if user_input:
    # st.subheader("Parameter Short Name")
    # st.write(long_name_to_short_name(user_input, df))
    short_name = long_name_to_short_name(user_input, df)
    st.text_area("Parameter Short Name", short_name, disabled=True)