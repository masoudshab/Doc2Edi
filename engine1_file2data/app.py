
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import pandas as pd
import json
import numpy as np


st.title("Invoice Extraction App")

uploaded_file = st.file_uploader('Choose your Invoice .pdf file', type="pdf")

if uploaded_file is not None:

    name_arr=[]
    value_arr=[]

    with open("test/header.json", "r") as json_file:
        json_dict = json.load(json_file)



    name_arr = np.array(list(json_dict.keys()))
    value_arr = np.array(list(json_dict.values()))

    with st.sidebar:
        st.text_input(name_arr[0],value=value_arr[0])
        st.text_input(name_arr[1], value=value_arr[1])
        st.text_input(name_arr[2], value=value_arr[2])
        st.text_input(name_arr[3], value=value_arr[3])
        st.text_input(name_arr[4], value=value_arr[4])
        st.text_input(name_arr[5], value=value_arr[5])
        st.text_input(name_arr[6], value=value_arr[6])
        st.text_input(name_arr[7], value=value_arr[7])
        st.text_input(name_arr[8], value=value_arr[8])
        st.text_input(name_arr[9], value=value_arr[9])

    df = pd.read_csv("test/Invoice.csv")


    gb = GridOptionsBuilder.from_dataframe(df)

    gb.configure_default_column(value=True, enableRowGroup=True, aggFunc=None, editable=True)

    gb.configure_selection(selection_mode="multiple", use_checkbox=True)

    GridOptions=gb.build()
    GridOptions["columnDefs"][0]["headerCheckboxSelection"]=True

    with st.form("table_form", clear_on_submit=False):
        grid_response = AgGrid(df, gridOptions=GridOptions, height=300,
        data_return_mode="AS_INPUT", update_mode='MODEL_CHANGED')                   #fit_columns_on_grid_load=True
        selected = grid_response['selected_rows']
        if st.form_submit_button("Submit"):
            df = pd.DataFrame(selected)
        else:
            df = grid_response['data']

    @st.cache
    def convert_df(df):
       return df.to_csv().encode('utf-8')


    csv = convert_df(df)

    st.download_button(
       "Press to Download",
       csv,
       "file.csv",
       "text/csv",
       key='download-csv'
    )

