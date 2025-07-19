import streamlit as st
from Bio import pairwise2
from Bio.Seq import Seq
import numpy as np
import matplotlib.pyplot as plt
import openai
from openai import OpenAI

# ⛳ Load OpenAI key securely
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 🧬 Alignment Methods
def needleman_wunsch(seq1, seq2):
    alignments = pairwise2.align.globalxx(seq1, seq2)
    return alignments[0]

def smith_waterman(seq1, seq2):
    alignments = pairwise2.align.localxx(seq1, seq2)
    return alignments[0]

def word_method(seq1, seq2, word_size=2):
    matches = []
    for i in range(len(seq1) - word_size + 1):
        word = seq1[i:i+word_size]
        for j in range(len(seq2) - word_size + 1):
            if seq2[j:j+word_size] == word:
                matches.append((i, j, word))
    return matches

def dot_matrix(seq1, seq2):
    matrix = np.zeros((len(seq1), len(seq2)))
    for i in range(len(seq1)):
        for j in range(len(seq2)):
            if seq1[i] == seq2[j]:
                matrix[i][j] = 1
    return matrix

# 🎨 Plotting Dot Matrix
def plot_dot_matrix(matrix, seq1, seq2):
    fig, ax = plt.subplots()
    ax.imshow(matrix, cmap='Greys', interpolation='nearest')
    ax.set_xticks(np.arange(len(seq2)))
    ax.set_yticks(np.arange(len(seq1)))
    ax.set_xticklabels(list(seq2))
    ax.set_yticklabels(list(seq1))
    st.pyplot(fig)

# 🧠 Chat with Gene Alignment Bot
def chat_with_bot(user_input):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a bioinformatics expert helping students learn gene sequence alignment."},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content

# 🧪 Streamlit UI
st.title("🧬 Gene Sequence Aligner + Chatbot")
st.markdown("Paste or upload two DNA sequences and choose an alignment method.")

# 📋 Input Method
option = st.radio("Input method", ["Paste Sequences", "Upload FASTA files"])

if option == "Paste Sequences":
    seq1 = st.text_area("Sequence 1", placeholder="ATCGATG...")
    seq2 = st.text_area("Sequence 2", placeholder="ATGCGT...")
else:
    uploaded1 = st.file_uploader("Upload Sequence 1", type=["fasta", "fa"])
    uploaded2 = st.file_uploader("Upload Sequence 2", type=["fasta", "fa"])
    if uploaded1 and uploaded2:
        from Bio import SeqIO
        seq1 = str(SeqIO.read(uploaded1, "fasta").seq)
        seq2 = str(SeqIO.read(uploaded2, "fasta").seq)
    else:
        seq1, seq2 = "", ""

# ⛓️ Alignment Method
method = st.selectbox("Choose alignment method", ["Needleman-Wunsch", "Smith-Waterman", "Word Method", "Dot Matrix"])

if st.button("Align Sequences"):
    if not seq1 or not seq2:
        st.error("Please provide both sequences.")
    else:
        if method == "Needleman-Wunsch":
            result = needleman_wunsch(seq1, seq2)
            st.code(result.seqA + "\n" + result.seqB)
        elif method == "Smith-Waterman":
            result = smith_waterman(seq1, seq2)
            st.code(result.seqA + "\n" + result.seqB)
        elif method == "Word Method":
            matches = word_method(seq1, seq2)
            for i, j, word in matches:
                st.write(f"Match '{word}' at Seq1[{i}] and Seq2[{j}]")
        elif method == "Dot Matrix":
            matrix = dot_matrix(seq1, seq2)
            plot_dot_matrix(matrix, seq1, seq2)

# 🤖 Chatbot
st.markdown("## 💬 Ask the Alignment Bot")
chat_input = st.text_input("Enter your question:")
if st.button("Ask"):
    if chat_input:
        reply = chat_with_bot(chat_input)
        st.success(reply)
