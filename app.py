import streamlit as st
from Bio import pairwise2, SeqIO
from Bio.pairwise2 import format_alignment
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="🧬 Gene Sequence Aligner", layout="wide")
st.title("🧬 Gene Sequence Aligner App")

# Input Option
option = st.radio("Choose Input Method", ["Upload FASTA", "Paste Sequences"])

# Input Sequences
if option == "Upload FASTA":
    file1 = st.file_uploader("Upload Sequence 1 (FASTA)", type=["fasta", "fa"])
    file2 = st.file_uploader("Upload Sequence 2 (FASTA)", type=["fasta", "fa"])
    if file1 and file2:
        seq1 = str(SeqIO.read(file1, "fasta").seq)
        seq2 = str(SeqIO.read(file2, "fasta").seq)
    else:
        seq1 = seq2 = ""
else:
    seq1 = st.text_area("Paste Sequence 1", height=100)
    seq2 = st.text_area("Paste Sequence 2", height=100)

# Alignment Method
method = st.selectbox("Select Alignment Method", ["Needleman-Wunsch", "Smith-Waterman", "Dot Matrix", "Word Method"])

# Align Button
if st.button("🔍 Run Alignment") and seq1 and seq2:
    if method == "Needleman-Wunsch":
        alignments = pairwise2.align.globalxx(seq1, seq2)
        st.code(format_alignment(*alignments[0]), language="text")

    elif method == "Smith-Waterman":
        alignments = pairwise2.align.localxx(seq1, seq2)
        st.code(format_alignment(*alignments[0]), language="text")

    elif method == "Word Method":
        def word_match(s1, s2, k=3):
            words1 = set(s1[i:i+k] for i in range(len(s1)-k+1))
            words2 = set(s2[i:i+k] for i in range(len(s2)-k+1))
            return words1 & words2
        matches = word_match(seq1, seq2)
        st.success(f"Matched {len(matches)} common k-mers")
        st.write(matches)

    elif method == "Dot Matrix":
        def dot_matrix(s1, s2):
            dot = np.zeros((len(s1), len(s2)))
            for i in range(len(s1)):
                for j in range(len(s2)):
                    if s1[i] == s2[j]:
                        dot[i][j] = 1
            return dot

        matrix = dot_matrix(seq1, seq2)
        fig, ax = plt.subplots()
        ax.imshow(matrix, cmap="Greys", interpolation="none")
        ax.set_xlabel("Sequence 2")
        ax.set_ylabel("Sequence 1")
        st.pyplot(fig)

# Chatbot Assistant
with st.expander("💬 Ask GeneBot for Help"):
    user_q = st.text_input("Ask a question:")
    if user_q:
        import openai
        openai.api_key = st.secrets.get("OPENAI_API_KEY", "sk-...")
        from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful tutor for gene sequence alignment."},
        {"role": "user", "content": user_q}
    ]
)

st.markdown("**Answer:** " + response.choices[0].message.content)
