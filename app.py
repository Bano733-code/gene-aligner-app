import streamlit as st
from Bio import SeqIO
import numpy as np
import pandas as pd
import io

st.set_page_config(page_title="🧬 Gene Sequence Aligner", layout="wide")

# Alignment functions
def dot_matrix(seq1, seq2, window=1, threshold=1):
    m, n = len(seq1), len(seq2)
    matrix = np.zeros((m, n), dtype=int)
    for i in range(m - window + 1):
        for j in range(n - window + 1):
            if seq1[i:i+window] == seq2[j:j+window]:
                matrix[i+window-1][j+window-1] = 1
    return matrix

def needleman_wunsch(seq1, seq2, match=1, mismatch=-1, gap=-2):
    m, n = len(seq1)+1, len(seq2)+1
    score = np.zeros((m, n), dtype=int)
    for i in range(m): score[i][0] = i * gap
    for j in range(n): score[0][j] = j * gap

    for i in range(1, m):
        for j in range(1, n):
            diag = score[i-1][j-1] + (match if seq1[i-1] == seq2[j-1] else mismatch)
            delete = score[i-1][j] + gap
            insert = score[i][j-1] + gap
            score[i][j] = max(diag, delete, insert)
    return score

def smith_waterman(seq1, seq2, match=1, mismatch=-1, gap=-2):
    m, n = len(seq1)+1, len(seq2)+1
    score = np.zeros((m, n), dtype=int)
    max_score = 0
    max_pos = (0, 0)

    for i in range(1, m):
        for j in range(1, n):
            diag = score[i-1][j-1] + (match if seq1[i-1] == seq2[j-1] else mismatch)
            delete = score[i-1][j] + gap
            insert = score[i][j-1] + gap
            score[i][j] = max(0, diag, delete, insert)
            if score[i][j] > max_score:
                max_score = score[i][j]
                max_pos = (i, j)
    return score

# FASTA Parser
def read_fasta(uploaded_file):
    fasta_text = uploaded_file.read().decode("utf-8")
    fasta_io = io.StringIO(fasta_text)
    for record in SeqIO.parse(fasta_io, "fasta"):
        return str(record.seq)

# App UI
st.title("🧬 Gene Sequence Aligner App")
st.markdown("Upload two FASTA files and choose alignment method:")

col1, col2 = st.columns(2)
with col1:
    fasta1 = st.file_uploader("Upload First FASTA File", type=["fasta"])
with col2:
    fasta2 = st.file_uploader("Upload Second FASTA File", type=["fasta"])

if fasta1 and fasta2:
    seq1 = read_fasta(fasta1)
    seq2 = read_fasta(fasta2)

    st.success("✅ FASTA files loaded successfully!")
    method = st.selectbox("Choose Alignment Method", ["Dot Matrix", "Needleman-Wunsch", "Smith-Waterman"])

    if st.button("🔍 Run Alignment"):
        st.subheader("🧪 Alignment Results")

        if method == "Dot Matrix":
            matrix = dot_matrix(seq1, seq2)
        elif method == "Needleman-Wunsch":
            matrix = needleman_wunsch(seq1, seq2)
        elif method == "Smith-Waterman":
            matrix = smith_waterman(seq1, seq2)

        df = pd.DataFrame(matrix)
        st.write("🔢 Scoring Matrix:")
        st.dataframe(df.style.background_gradient(cmap='YlGnBu', axis=None))

        st.success("✅ Alignment completed.")

else:
    st.info("📂 Please upload both FASTA files to continue.")

st.markdown("---")
st.caption("Built with ❤️ for bioinformatics students")
