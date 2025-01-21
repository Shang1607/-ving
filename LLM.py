import pandas as pd
import streamlit as st
import openai
from transformers import pipeline

# Set OpenAI API key directly (replace with your actual key)
openai.api_key = "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"

def LLM():
    st.title("LLM Q&A with Dataset")

    # Upload dataset
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("### Dataset Preview")
        st.dataframe(df)

        # User input for question
        question = st.text_input("Ask a question about the dataset:")
        if question:
            st.write(f"You asked: {question}")

            # Choose the LLM to use
            llm_choice = st.radio("Select LLM to use:", ["OpenAI GPT", "Hugging Face Transformers"])

            if llm_choice == "OpenAI GPT":
                # Generate answer using OpenAI GPT
                try:
                    prompt = f"The following is a dataset:\n{df.head(5)}\n\nQuestion: {question}\nAnswer:"
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",  # Use gpt-4 if supported
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant for analyzing datasets."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=100,
                    )
                    answer = response["choices"][0]["message"]["content"].strip()
                    st.write("### OpenAI GPT Answer")
                    st.write(answer)
                except Exception as e:
                    st.error(f"Error with OpenAI GPT: {e}")

            elif llm_choice == "Hugging Face Transformers":
                # Generate answer using Hugging Face Transformers
                try:
                    qa_pipeline = pipeline("question-answering", model="distilbert-base-cased")
                    context = df.to_string()
                    result = qa_pipeline(question=question, context=context)
                    st.write("### Hugging Face Transformers Answer")
                    st.write(result["answer"])
                except Exception as e:
                    st.error(f"Error with Hugging Face Transformers: {e}")

            # Highlight relevant data
            st.write("### Highlighted Dataset")
            # Dummy logic to find relevant column
            # Replace this with actual logic based on LLM response
            relevant_column = df.columns[0]  # Default to first column
            st.write(f"Relevant Column: {relevant_column}")
            st.dataframe(df[[relevant_column]])
