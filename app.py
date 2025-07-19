import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Bio import pairwise2
from Bio.Seq import Seq
from Bio import SeqIO
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login

# Load HuggingFace model
@st.cache_resource
def load_chatbot():
    login(token=st.secrets["HF_TOKEN"])
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")
    model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")
    return tokenizer, model

tokenizer, model = load_chatbot()

def chatbot_response(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=100)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Dot Matrix Method
def dot_matrix(seq1, seq2, window=1):
    matrix = np.zeros((len(seq1), len(seq2)))
    for i in range(len(seq1) - window + 1):
        for j in range(len(seq2) - window + 1):
            if seq1[i:i+window] == seq2[j:j+window]:
                matrix[i][j] = 1
    return matrix

# Word Method (k-mer match)
def word_method(seq1, seq2, k=3):
    matches = []
    for i in range(len(seq1) - k + 1):
        kmer = seq1[i:i+k]
        for j in range(len(seq2) - k + 1):
            if kmer == seq2[j:j+k]:
                matches.append((i, j, kmer))
    return matches

st.title("🧬 Gene Sequence Aligner App + 🤖 Chatbot")

# File upload
st.sidebar.header("Upload FASTA files")
file1 = st.sidebar.file_uploader("Sequence 1 (FASTA)", type=["fasta"])
file2 = st.sidebar.file_uploader("Sequence 2 (FASTA)", type=["fasta"])

# Text input fallback
st.sidebar.markdown("Or paste sequences manually:")
seq1_text = st.sidebar.text_area("Paste Sequence 1")
seq2_text = st.sidebar.text_area("Paste Sequence 2")

# Alignment method
method = st.selectbox("Choose alignment method", [
    "Dot Matrix",
    "Needleman-Wunsch",
    "Smith-Waterman",
    "Word Method"
])

# Load sequences
def load_sequence(f, fallback):
    if f:
        for record in SeqIO.parse(f, "fasta"):
            return str(record.seq)
    return fallback.strip()

seq1 = load_sequence(file1, seq1_text)
seq2 = load_sequence(file2, seq2_text)

if st.button("Align Sequences"):
    if not seq1 or not seq2:
        st.warning("Please provide both sequences.")
    else:
        if method == "Dot Matrix":
            matrix = dot_matrix(seq1, seq2)
            fig, ax = plt.subplots(figsize=(8,6))
            ax.imshow(matrix, cmap="gray", interpolation="nearest")
            ax.set_title("Dot Matrix Alignment")
            st.pyplot(fig)

        elif method == "Needleman-Wunsch":
            alignments = pairwise2.align.globalxx(seq1, seq2)
            st.code(alignments[0].format())

        elif method == "Smith-Waterman":
            alignments = pairwise2.align.localxx(seq1, seq2)
            st.code(alignments[0].format())

        elif method == "Word Method":
            matches = word_method(seq1, seq2)
            df = pd.DataFrame(matches, columns=["Seq1_Pos", "Seq2_Pos", "k-mer"])
            st.write(df)

# Chatbot
st.header("🤖 Ask Bio-Chatbot Anything")
user_input = st.text_input("Ask your question")
if st.button("Get Response"):
    if user_input:
        with st.spinner("Thinking..."):
            response = chatbot_response(user_input)
            st.success(response)
    else:
        st.warning("Please enter a question.")
