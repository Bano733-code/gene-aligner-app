import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login
import os

# Load Hugging Face token securely from Streamlit secrets
HF_TOKEN = st.secrets["HF_TOKEN"]

# Login to Hugging Face Hub
login(token=HF_TOKEN)

@st.cache_resource
def load_chatbot():
    tokenizer = AutoTokenizer.from_pretrained(
        "mistralai/Mistral-7B-Instruct-v0.1",
        token=HF_TOKEN
    )
    model = AutoModelForCausalLM.from_pretrained(
        "mistralai/Mistral-7B-Instruct-v0.1",
        token=HF_TOKEN
    )
    return tokenizer, model

tokenizer, model = load_chatbot()

# Streamlit UI
st.set_page_config(page_title="Gene Sequence Aligner + Chatbot")
st.title("🧬 Gene Sequence Aligner + 🧠 Bio Chatbot")

# Input DNA/RNA sequences
seq1 = st.text_area("🔹 Sequence 1", height=100)
seq2 = st.text_area("🔸 Sequence 2", height=100)

# Chatbot Input
st.markdown("### 💬 Ask the Gene Chatbot")
user_input = st.text_input("Type your question here")

# Chatbot Output
if user_input:
    prompt = f"<s>[INST] {user_input} [/INST]"
    inputs = tokenizer(prompt, return_tensors="pt")
    output = model.generate(**inputs, max_new_tokens=256)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    st.success(response)

# (OPTIONAL) Alignment selection dropdown
alignment_method = st.selectbox("Choose Alignment Method", [
    "Dot Matrix", "Needleman-Wunsch", "Smith-Waterman", "Word Method"
])

# Alignment (not implemented yet)
if st.button("🔍 Align Sequences"):
    st.info(f"Alignment using: {alignment_method}")
    st.warning("🧪 Alignment logic not implemented in this version.")
