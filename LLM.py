import os
import pandas as pd
import streamlit as st
import openai
from transformers import pipeline


openai.api_key = os.environ.get ("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")

def LLM():
    st.title("LLM Q&A with Dataset")

    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("### Dataset Preview")
        st.dataframe(df.head(10))

        question = st.text_input("Ask a question about the dataset:")
        llm_choice = st.radio("Select LLM to use:", ["OpenAI GPT", "Hugging Face Transformers"])

        if question:
            st.write(f"You asked: {question}")

            if llm_choice == "OpenAI GPT":
                try:
                    context_str = df.head(20).to_string()
                    messages = [
                        {"role": "system", "content": "You are a helpful assistant for analyzing datasets."},
                        {"role": "user", "content": f"The following is a dataset sample:\n{context_str}\n\nQuestion: {question}"}
                    ]
                    # Note: "gpt-4" is the correct name (you must have GPT-4 API access)
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=messages,
                        max_tokens=150
                    )
                    answer = response.choices[0].message.content.strip()
                    st.write("### OpenAI GPT Answer")
                    st.write(answer)
                except Exception as e:
                    st.error(f"Error with OpenAI GPT: {e}")

            else:  # Hugging Face Transformers
                try:
                    qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
                    context_str = df.head(30).to_string()
                    result = qa_pipeline(question=question, context=context_str)
                    st.write("### Hugging Face Transformers Answer")
                    st.write(result["answer"])
                except Exception as e:
                    st.error(f"Error with Hugging Face Transformers: {e}")

            st.write("### Highlighted Dataset")
            relevant_column = df.columns[0]
            st.write(f"Relevant Column: {relevant_column}")
            st.dataframe(df[[relevant_column]])