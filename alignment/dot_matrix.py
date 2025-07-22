import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

def plot_dot_matrix(seq1, seq2, window=1):
    matrix = np.zeros((len(seq1), len(seq2)))
    for i in range(len(seq1) - window + 1):
        for j in range(len(seq2) - window + 1):
            if seq1[i:i+window] == seq2[j:j+window]:
                matrix[i][j] = 1
    fig, ax = plt.subplots()
    ax.imshow(matrix, cmap="Greys", interpolation="none")
    ax.set_xlabel("Sequence B")
    ax.set_ylabel("Sequence A")
    st.pyplot(fig)
