import streamlit as st
import pandas as pd

def dataset():
    st.title("Dataset Filtering Dashboard")

    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file:
        # Load dataset
        df = pd.read_csv(uploaded_file)
        st.write("### Original Dataset:")
        st.dataframe(df)

        # Make a copy for filtering
        filtered_df = df.copy()

        # Categorical filtering
        st.write("### Filter by Categorical Columns:")
        categorical_columns = df.select_dtypes(include=["object", "category"]).columns

        for col in categorical_columns:
            unique_values = df[col].unique()
            selected_values = st.multiselect(f"Filter {col} by:", unique_values)
            if selected_values:
                filtered_df = filtered_df[filtered_df[col].isin(selected_values)]

        # Numeric filtering
        st.write("### Filter by Numeric Columns:")
        numeric_columns = df.select_dtypes(include=["number"]).columns

        for col in numeric_columns:
            min_value = float(df[col].min())
            max_value = float(df[col].max())
            range_selected = st.slider(
                f"Select range for {col}:", min_value, max_value, (min_value, max_value)
            )
            filtered_df = filtered_df[filtered_df[col].between(range_selected[0], range_selected[1])]

        # Display filtered dataset
        if filtered_df.empty:
            st.warning("No data available after filtering.")
        else:
            st.write("### Filtered Dataset:")
            st.dataframe(filtered_df)

            # Download filtered dataset
            csv = filtered_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download Filtered Dataset",
                data=csv,
                file_name="filtered_dataset.csv",
                mime="text/csv",
            )
