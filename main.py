import streamlit as st
from home import show_home
from file_upload import show_file_upload
from to_do_list import show_to_do_list
from calculator import show_calculator
from public_Api import public_Api

st.sidebar.header('Navigator')
page = st.sidebar.selectbox('Select a page', ['Home', 
                                              'File Upload', 
                                              'To do list', 
                                              'Calculator', 
                                              'Public API'])

if page == 'Home':
    show_home()
elif page == 'Calculator':
    show_calculator()    
elif page == 'File Upload':
    show_file_upload()
elif page == 'To do list':
    show_to_do_list()
elif page == 'Public API':
    public_Api()
