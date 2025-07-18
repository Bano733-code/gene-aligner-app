import streamlit as st
import numpy as np
from Bio import pairwise2
from Bio.Seq import Seq
from Bio import SeqIO
import io

st.set_page_config(page_title="Gene Sequence Aligner", layout="centered")

st.title("🧬 Gene Sequence Aligner")
st.markdown("Align DNA/RNA sequences using different methods.")

# Choose input mode
input_mode = st.radio("Choose Input Method", ["📁 Upload FASTA Files", "✍️ Paste Sequences"])

def read_fasta(file):
    try:
        record = next(SeqIO.parse(file, "fasta"))
        return str(record.seq)
    except Exception as e:
        st.error(f"Error reading FASTA file: {e}")
        return None

# Get sequences
seq1, seq2 = None, None

if input_mode == "📁 Upload FASTA Files":
    fasta1 = st.file_uploader("Upload Sequence 1 (FASTA)", type=["fasta", "fa"])
    fasta2 = st.file_uploader("Upload Sequence 2 (FASTA)", type=["fasta", "fa"])

    if fasta1 and fasta2:
        seq1 = read_fasta(fasta1)
        seq2 = read_fasta(fasta2)

elif input_mode == "✍️ Paste Sequences":
    seq1 = st.text_area("Paste Sequence 1", height=100)
    seq2 = st.text_area("Paste Sequence 2", height=100)

# Choose alignment method
if seq1 and seq2:
    method = st.selectbox("Choose Alignment Method", ["Needleman-Wunsch", "Smith-Waterman"])

    if st.button("🔬 Align Sequences"):
        seq1 = seq1.replace("\n", "").strip().upper()
        seq2 = seq2.replace("\n", "").strip().upper()

        if method == "Needleman-Wunsch":
            alignments = pairwise2.align.globalxx(seq1, seq2)
        else:
            alignments = pairwise2.align.localxx(seq1, seq2)

        top = alignments[0]
        st.subheader("✅ Best Alignment")
        st.code(f"{top.seqA}\n{top.seqB}\nScore: {top.score}")
else:
    st.info("👆 Upload or paste two sequences to begin.")

st.markdown("---")
st.markdown("🧪 Built with Biopython + Streamlit")

