import streamlit as st

def show_to_do_list():
    st.title('To do list')
    st.write('This is a simple to do list that allows you to add and remove items')

    if 'tasks' not in st.session_state:
        st.session_state.tasks = ["Example task",]

    new_task = st.text_input('Enter a new task')
    if st.button('Add task'):
        if new_task:
            st.session_state.tasks.append(new_task)
            st.write(f"Added task: {new_task}")

    st.write('### Tasks:')
    completed_tasks = []
    for i, task in enumerate(st.session_state.tasks):
        if st.checkbox(task, key=f'task_{i}'):
            completed_tasks.append(task)

    if st.button('Clear completed tasks'):
        st.session_state.tasks = [task for task in st.session_state.tasks if task not in completed_tasks]
        st.rerun()