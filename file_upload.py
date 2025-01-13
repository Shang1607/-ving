import streamlit as st
import pandas as pd
import plotly.express as px

def show_file_upload():
    st.title('Practicing file uploading, numeric operations, and visualization')
    
    if 'reset' not in st.session_state:
        st.session_state.reset = False

    Uploaded = st.file_uploader('Upload a file', type=['csv', 'xlsx'])

    if Uploaded:
        if st.session_state.reset:
            st.session_state.reset = False

        try:
            if Uploaded.name.endswith('.csv'):
                df = pd.read_csv(Uploaded)
            elif Uploaded.name.endswith('.xlsx'):
                df = pd.read_excel(Uploaded)
            else:
                st.error("Unsupported file type.")
                st.stop()
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.stop()

            head = st.checkbox('Show the first 5 rows', key='head')
            if head:
                st.write(df.head())
            tail = st.checkbox('Show the last 5 rows', key='tail')
            if tail:
                st.write(df.tail())
            describe = st.checkbox('Show the description', key='describe')
            if describe:
                st.write(df.describe())

            numeric_columns = df.select_dtypes(include=['number']).columns
            selected_column = st.selectbox('Select a column', numeric_columns)
            st.write(df[selected_column].describe())

            bins = st.slider('Select the number of bins', 5, 50, 10)
            fig = px.histogram(df, x=selected_column, nbins=bins)
            st.plotly_chart(fig)