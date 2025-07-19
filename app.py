import streamlit as st
from Bio import pairwise2
from Bio.Seq import Seq
import numpy as np
import matplotlib.pyplot as plt
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Hugging Face chatbot setup
@st.cache_resource
def load_chatbot():
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1", use_auth_token=True)
    model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1", device_map="auto", torch_dtype=torch.float16, use_auth_token=True)
    return tokenizer, model

tokenizer, model = load_chatbot()

def chatbot_response(user_msg):
    input_ids = tokenizer.encode(user_msg, return_tensors="pt").to("cuda")
    output = model.generate(input_ids, max_new_tokens=200, pad_token_id=tokenizer.eos_token_id)
    return tokenizer.decode(output[0], skip_special_tokens=True)

# UI
st.title("🧬 Gene Sequence Aligner + Chatbot")

tab1, tab2 = st.tabs(["🔬 Alignment Tool", "🤖 Gene Chatbot"])

with tab1:
    st.subheader("Enter or Upload Gene Sequences")

    seq1 = st.text_area("🔠 Sequence 1")
    seq2 = st.text_area("🔡 Sequence 2")
    uploaded_file = st.file_uploader("📂 Or Upload FASTA File (2 sequences)", type=["fasta", "fa"])

    if uploaded_file is not None:
        contents = uploaded_file.read().decode("utf-8").split(">")
        sequences = [s.strip().split("\n", 1)[1].replace("\n", "") for s in contents if s]
        if len(sequences) >= 2:
            seq1, seq2 = sequences[:2]

    method = st.selectbox("🧬 Choose Alignment Method", ["Dot Matrix", "Needleman-Wunsch", "Smith-Waterman", "Word Method"])

    if st.button("🔍 Align"):
        if method == "Dot Matrix":
            window = 3
            threshold = 2
            x, y = len(seq1), len(seq2)
            dot_matrix = np.zeros((x - window + 1, y - window + 1))
            for i in range(x - window + 1):
                for j in range(y - window + 1):
                    match = sum(seq1[i + k] == seq2[j + k] for k in range(window))
                    if match >= threshold:
                        dot_matrix[i][j] = 1
            fig, ax = plt.subplots()
            ax.imshow(dot_matrix, cmap="Greys", origin="lower")
            ax.set_xlabel("Sequence 2")
            ax.set_ylabel("Sequence 1")
            st.pyplot(fig)

        elif method == "Needleman-Wunsch":
            alignments = pairwise2.align.globalxx(seq1, seq2)
            st.code(pairwise2.format_alignment(*alignments[0]))

        elif method == "Smith-Waterman":
            alignments = pairwise2.align.localxx(seq1, seq2)
            st.code(pairwise2.format_alignment(*alignments[0]))

        elif method == "Word Method":
            k = 3
            words1 = set(seq1[i:i+k] for i in range(len(seq1)-k+1))
            words2 = set(seq2[i:i+k] for i in range(len(seq2)-k+1))
            common = words1.intersection(words2)
            st.write(f"Common {k}-mers: {common}")
            st.write(f"Total matches: {len(common)}")

with tab2:
    st.subheader("🤖 Ask About Gene Concepts")

    user_input = st.text_input("💬 Ask your question:")
    if st.button("🧠 Respond"):
        with st.spinner("Thinking..."):
            reply = chatbot_response(user_input)
            st.success(reply)
