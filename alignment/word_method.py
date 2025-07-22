import streamlit as st

def word_alignment(seq1, seq2, word_size=3):
    matches = []
    for i in range(len(seq1) - word_size + 1):
        word = seq1[i:i+word_size]
        for j in range(len(seq2) - word_size + 1):
            if word == seq2[j:j+word_size]:
                matches.append((i, j, word))
    if matches:
        st.write(f"Found {len(matches)} matching words:")
        for match in matches:
            st.write(f"SeqA[{match[0]}] = SeqB[{match[1]}] → {match[2]}")
    else:
        st.write("No matching words found.")
