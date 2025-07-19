import streamlit as st
import numpy as np
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# -----------------------------
# Chatbot Loader (Lightweight)
# -----------------------------
@st.cache_resource
def load_chatbot():
    tokenizer = AutoTokenizer.from_pretrained("tiiuae/falcon-rw-1b")
    model = AutoModelForCausalLM.from_pretrained("tiiuae/falcon-rw-1b")
    return tokenizer, model

tokenizer, model = load_chatbot()

# -----------------------------
# Dot Matrix Alignment
# -----------------------------
def dot_matrix(seq1, seq2, window=1, threshold=1):
    matrix = np.zeros((len(seq1), len(seq2)))
    for i in range(len(seq1) - window + 1):
        for j in range(len(seq2) - window + 1):
            if seq1[i:i+window] == seq2[j:j+window]:
                matrix[i][j] = 1
    return matrix

# -----------------------------
# Needleman-Wunsch Alignment
# -----------------------------
def needleman_wunsch(seq1, seq2, match=1, mismatch=-1, gap=-2):
    m, n = len(seq1), len(seq2)
    score = np.zeros((m+1, n+1))

    for i in range(m+1):
        score[i][0] = i * gap
    for j in range(n+1):
        score[0][j] = j * gap

    for i in range(1, m+1):
        for j in range(1, n+1):
            diag = score[i-1][j-1] + (match if seq1[i-1] == seq2[j-1] else mismatch)
            delete = score[i-1][j] + gap
            insert = score[i][j-1] + gap
            score[i][j] = max(diag, delete, insert)

    return score

# -----------------------------
# Smith-Waterman Alignment
# -----------------------------
def smith_waterman(seq1, seq2, match=1, mismatch=-1, gap=-2):
    m, n = len(seq1), len(seq2)
    score = np.zeros((m+1, n+1))

    max_score = 0
    for i in range(1, m+1):
        for j in range(1, n+1):
            diag = score[i-1][j-1] + (match if seq1[i-1] == seq2[j-1] else mismatch)
            delete = score[i-1][j] + gap
            insert = score[i][j-1] + gap
            score[i][j] = max(0, diag, delete, insert)
            max_score = max(max_score, score[i][j])
    return score

# -----------------------------
# Word Method (Naive)
# -----------------------------
def word_method(seq1, seq2, word_size=3):
    matches = []
    for i in range(len(seq1) - word_size + 1):
        word = seq1[i:i+word_size]
        for j in range(len(seq2) - word_size + 1):
            if word == seq2[j:j+word_size]:
                matches.append((i, j))
    return matches

# -----------------------------
# Chatbot Function
# -----------------------------
def chatbot_reply(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=100)
    reply = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return reply

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="🧬 Gene Sequence Aligner App", layout="centered")
st.title("🧬 Gene Sequence Aligner App")
st.write("Paste two DNA/RNA sequences and choose an alignment method.")

seq1 = st.text_area("🔬 Paste Sequence 1", height=100)
seq2 = st.text_area("🧪 Paste Sequence 2", height=100)
method = st.selectbox("🛠️ Choose Alignment Method", ["Dot Matrix", "Needleman-Wunsch", "Smith-Waterman", "Word Method"])

if st.button("🔍 Align Sequences"):
    if not seq1 or not seq2:
        st.warning("Please paste both sequences!")
    else:
        st.subheader("🧾 Result:")
        if method == "Dot Matrix":
            matrix = dot_matrix(seq1, seq2)
            st.write(matrix)
        elif method == "Needleman-Wunsch":
            score = needleman_wunsch(seq1, seq2)
            st.write(score)
        elif method == "Smith-Waterman":
            score = smith_waterman(seq1, seq2)
            st.write(score)
        elif method == "Word Method":
            matches = word_method(seq1, seq2)
            st.write("Matching word positions:", matches)

# -----------------------------
# Chatbot Interface
# -----------------------------
st.markdown("---")
st.header("💬 Ask Bio Chatbot")
chat_input = st.text_input("Ask me anything about alignment, bioinformatics, or DNA...")
if st.button("🤖 Get Reply"):
    if chat_input:
        with st.spinner("Generating reply..."):
            response = chatbot_reply(chat_input)
        st.success(response)
