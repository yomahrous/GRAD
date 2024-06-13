import streamlit as st
import json
from transformers import pipeline

# Load the fine-tuned model
pipe = pipeline("question-answering", model="salti/bert-base-multilingual-cased-finetuned-squad")

# Load your dataset
with open("C:/Users/momeh/OneDrive/Desktop/merged_arcd.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Get titles for later use
titles = [item["title"] for item in data["data"]]

# Streamlit interface for question input
user_question = st.text_input("Enter your question here:")

if st.button("Answer"):
    # Simple keyword matching to select title
    selected_title = None
    highest_match_count = 0

    # Count occurrences of each word in the title within the question
    for title in titles:
        match_count = sum(word.lower() in user_question.lower() for word in title.split())
        if match_count > highest_match_count:
            highest_match_count = match_count
            selected_title = title

    # Find contexts for the selected title
    if selected_title:
        selected_contexts = next(item for item in data["data"] if item["title"] == selected_title)["paragraphs"]
        # Concatenate all paragraphs to use as the context
        selected_context = " ".join([context["context"] for context in selected_contexts])

        # Prepare input for the model
        model_input = {
            'question': user_question,
            'context': selected_context
        }
        # Get the answer from the model
        answer = pipe(model_input)
        st.write("Answer:", answer['answer'])
    else:
        st.write("No relevant title found. Please rephrase your question.")

# Run the streamlit app from the terminal:
# streamlit run your_script_name.py 