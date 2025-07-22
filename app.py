import streamlit as st
import pandas as pd
from alignment.needleman_wunsch import needleman_wunsch
from alignment.smith_waterman import smith_waterman
from alignment.dot_matrix import plot_dot_matrix
from alignment.word_method import word_alignment
from Bio import SeqIO
import io

st.title("🧬 GeneAligner: Bioinformatics Sequence Alignment Tool")

st.subheader("📁 Upload or Paste Sequences")

uploaded_file1 = st.file_uploader("Upload Sequence A (FASTA, GenBank, TXT)", type=["fasta", "fa", "gb", "txt"])
uploaded_file2 = st.file_uploader("Upload Sequence B (FASTA, GenBank, TXT)", type=["fasta", "fa", "gb", "txt"])

def read_sequence(uploaded_file):
    if uploaded_file:
        content = uploaded_file.read().decode("utf-8")
        file_type = uploaded_file.name.split(".")[-1].lower()

        if file_type in ["fa", "fasta"]:
            lines = content.splitlines()
            return "".join([line for line in lines if not line.startswith(">")])
        elif file_type == "gb":
            try:
                record = SeqIO.read(io.StringIO(content), "genbank")
                return str(record.seq)
            except:
                return ""
        elif file_type == "txt":
            return content.replace("\n", "").strip()
    return ""

seq1 = read_sequence(uploaded_file1) or st.text_area("Or paste Sequence A", height=150)
seq2 = read_sequence(uploaded_file2) or st.text_area("Or paste Sequence B", height=150)

method = st.selectbox("🔧 Choose Alignment Method", 
                      ["Dot Matrix", "Needleman-Wunsch", "Smith-Waterman", "Word Method"])

if st.button("🔍 Align Sequences"):
    if not seq1 or not seq2:
        st.warning("Please input both sequences.")
    else:
        align1, align2 = "", ""
        if method == "Dot Matrix":
            plot_dot_matrix(seq1, seq2)
        elif method == "Needleman-Wunsch":
            score, align1, align2 = needleman_wunsch(seq1, seq2)
            st.write(f"**Global Alignment Score:** {score}")
        elif method == "Smith-Waterman":
            score, align1, align2 = smith_waterman(seq1, seq2)
            st.write(f"**Local Alignment Score:** {score}")
        elif method == "Word Method":
            word_alignment(seq1, seq2, word_size=3)

        if align1 and align2:
            st.code(align1)
            st.code(align2)

            df = pd.DataFrame({
                "Sequence A": list(align1),
                "Sequence B": list(align2)
            })
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Alignment as CSV",
                data=csv,
                file_name="alignment_result.csv",
                mime="text/csv"
            )
