import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

def pipeline():
    st.title("Data Upload and Processing Pipeline")

    # Upload dataset
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            if df.empty:
                st.error("The uploaded file is empty. Please upload a valid CSV file.")
                return

            st.write("### Original Dataset:")
            st.dataframe(df)

            # Preprocessing pipeline
            if "processed_df" not in st.session_state:
                st.session_state.processed_df = df.copy()
            processed_df = st.session_state.processed_df

            if st.checkbox("Remove duplicates"):
                processed_df.drop_duplicates(inplace=True)
                st.success("Duplicates removed!")
                st.dataframe(processed_df)

            missing_option = st.selectbox(
                "Handle missing values:", ["None", "Fill with value", "Drop rows"]
            )
            if missing_option == "Fill with value":
                fill_value = st.text_input("Enter value to fill missing data", "N/A")
                processed_df.fillna(fill_value, inplace=True)
                st.success("Missing values filled!")
            elif missing_option == "Drop rows":
                processed_df.dropna(inplace=True)
                st.success("Rows with missing values dropped!")
            st.dataframe(processed_df)

            if st.checkbox("Normalize Data"):
                numeric_columns = processed_df.select_dtypes(include=["number"]).columns
                selected_columns = st.multiselect(
                    "Select numeric columns to normalize:", numeric_columns
                )
                if selected_columns:
                    scaler = MinMaxScaler()
                    processed_df[selected_columns] = scaler.fit_transform(
                        processed_df[selected_columns]
                    )
                    st.success("Selected columns normalized!")
                st.dataframe(processed_df)

            if st.checkbox("Show Summary Statistics"):
                st.write(processed_df.describe())

            if st.checkbox("Visualize Data"):
                numeric_columns = processed_df.select_dtypes(include=["number"]).columns
                if numeric_columns.empty:
                    st.warning("No numeric columns available for visualization.")
                else:
                    selected_column = st.selectbox("Select a column to visualize:", numeric_columns)
                    fig, ax = plt.subplots()
                    ax.hist(processed_df[selected_column], bins=20)
                    st.pyplot(fig)

            # Download processed dataset
            csv = processed_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download Processed Dataset",
                data=csv,
                file_name="processed_dataset.csv",
                mime="text/csv",
            )
        except Exception as e:
            st.error(f"An error occurred: {e}")
