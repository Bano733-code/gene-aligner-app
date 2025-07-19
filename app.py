import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

st.set_page_config(page_title="Gene Aligner + Chatbot", layout="wide")

@st.cache_resource
def load_chatbot():
    tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
    model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
    return tokenizer, model

tokenizer, model = load_chatbot()

st.title("🧬 Gene Aligner + 🤖 Chatbot")

with st.expander("💬 Chat with BioBot"):
    user_input = st.text_input("Ask me anything about gene alignment, sequences, or bioinformatics")

    if user_input:
        # Encode user input and add to chat history
        input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")

        # Generate response
        chat_history_ids = model.generate(
            input_ids,
            max_length=1000,
            pad_token_id=tokenizer.eos_token_id,
            no_repeat_ngram_size=3,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.75,
        )

        # Decode and display
        response = tokenizer.decode(chat_history_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
        st.markdown(f"**BioBot:** {response}")
