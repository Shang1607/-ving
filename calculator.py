import streamlit as st

def show_calculator():    
    st.title('Calculator')
    st.write('This is a simple calculator that takes two numbers and performs a simple operation on them')

    num1 = st.number_input('Enter the first number')
    num2 = st.number_input('Enter the second number')

    operation = st.selectbox('Choose an operation', ['Add', 'Subtract', 'Multiply', 'Divide'])

    if st.button('Calculate'):
        if operation == 'Add':  
            result = num1 + num2    
        elif operation == 'Subtract':
            result = num1 - num2
        elif operation == 'Multiply':
            result = num1 * num2
        elif operation == 'Divide':
            result = num1 / num2
            st.write(f'The totalt is {result}')