import streamlit as st
import pandas as pd
from alignment.needleman_wunsch import needleman_wunsch
from alignment.smith_waterman import smith_waterman
from alignment.dot_matrix import plot_dot_matrix
from alignment.word_method import word_alignment
from Bio import SeqIO
import io

st.set_page_config(page_title="GeneAligner", layout="wide")
st.title("🧬 GeneAligner: Bioinformatics Sequence Alignment Tool")

uploaded_file1 = st.file_uploader("Upload Sequence A (FASTA, GenBank, TXT)", type=["fasta", "fa", "gb", "txt"])
uploaded_file2 = st.file_uploader("Upload Sequence B (FASTA, GenBank, TXT)", type=["fasta", "fa", "gb", "txt"])

def read_sequence(uploaded_file):
    if uploaded_file:
        content = uploaded_file.read().decode("utf-8")
        file_type = uploaded_file.name.split(".")[-1].lower()
        if file_type in ["fa", "fasta"]:
            return "".join([line for line in content.splitlines() if not line.startswith(">")])
        elif file_type == "gb":
            try:
                record = SeqIO.read(io.StringIO(content), "genbank")
                return str(record.seq)
            except:
                return ""
        elif file_type == "txt":
            return content.replace("\n", "").strip()
    return ""

# Alignment match line generator
def get_match_line(seq1, seq2):
    line = ""
    for a, b in zip(seq1, seq2):
        if a == b:
            line += "|"
        elif a == "-" or b == "-":
            line += " "
        else:
            line += "."
    return line

# Color-coded HTML alignment
def render_alignment_with_color(seq1, seq2):
    html_seq1, html_seq2 = "", ""
    for a, b in zip(seq1, seq2):
        if a == b:
            html_seq1 += f'<span style="color:green">{a}</span>'
            html_seq2 += f'<span style="color:green">{b}</span>'
        elif a == "-" or b == "-":
            html_seq1 += f'<span style="color:gray">{a}</span>'
            html_seq2 += f'<span style="color:gray">{b}</span>'
        else:
            html_seq1 += f'<span style="color:red">{a}</span>'
            html_seq2 += f'<span style="color:red">{b}</span>'
    st.markdown("#### 🔬 Aligned Sequences (Colored)", unsafe_allow_html=True)
    st.markdown(f"<code>{html_seq1}</code>", unsafe_allow_html=True)
    st.markdown(f"<code>{html_seq2}</code>", unsafe_allow_html=True)

# Inputs
seq1 = read_sequence(uploaded_file1) or st.text_area("Or paste Sequence A", height=150)
seq2 = read_sequence(uploaded_file2) or st.text_area("Or paste Sequence B", height=150)

method = st.selectbox("🔧 Choose Alignment Method", 
                      ["Dot Matrix", "Needleman-Wunsch", "Smith-Waterman", "Word Method"])

if st.button("🔍 Align Sequences"):
    if not seq1 or not seq2:
        st.warning("Please input both sequences.")
    else:
        align1 = align2 = ""
        if method == "Dot Matrix":
            plot_dot_matrix(seq1, seq2)
        elif method == "Needleman-Wunsch":
            score, align1, align2, matrix = needleman_wunsch(seq1, seq2)
            st.write(f"**Global Alignment Score:** {score}")
            
            # Show Scoring Matrix
            st.markdown("#### 🧮 Alignment Scoring Matrix")
            df_matrix = pd.DataFrame(matrix, 
                                     index=["-"] + list(seq1), 
                                     columns=["-"] + list(seq2))
            st.dataframe(df_matrix.style.background_gradient(cmap='Blues'))
        elif method == "Smith-Waterman":
            score, align1, align2 = smith_waterman(seq1, seq2)
            st.write(f"**Local Alignment Score:** {score}")
        elif method == "Word Method":
            word_alignment(seq1, seq2, word_size=3)

        # Output alignment if available
        if align1 and align2:
            st.markdown("#### 🧬 Aligned Sequences")
            st.code(align1)
            st.code(get_match_line(align1, align2))
            st.code(align2)

            render_alignment_with_color(align1, align2)

            # Download as CSV
            df = pd.DataFrame({"Sequence A": list(align1), "Sequence B": list(align2)})
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download Alignment as CSV", csv, "alignment_result.csv", "text/csv")
