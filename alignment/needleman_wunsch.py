import numpy as np

def needleman_wunsch(seq1, seq2, match=1, mismatch=-1, gap=-2):
    m, n = len(seq1), len(seq2)
    score_matrix = np.zeros((m + 1, n + 1), dtype=int)

    # Initialize first row and column
    for i in range(m + 1):
        score_matrix[i][0] = i * gap
    for j in range(n + 1):
        score_matrix[0][j] = j * gap

    # Fill the score matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match_score = match if seq1[i - 1] == seq2[j - 1] else mismatch
            score_matrix[i][j] = max(
                score_matrix[i - 1][j - 1] + match_score,
                score_matrix[i - 1][j] + gap,
                score_matrix[i][j - 1] + gap
            )

    # Traceback
    align1, align2 = "", ""
    i, j = m, n
    while i > 0 and j > 0:
        current = score_matrix[i][j]
        diag = score_matrix[i - 1][j - 1]
        up = score_matrix[i - 1][j]
        left = score_matrix[i][j - 1]

        match_score = match if seq1[i - 1] == seq2[j - 1] else mismatch
        if current == diag + match_score:
            align1 = seq1[i - 1] + align1
            align2 = seq2[j - 1] + align2
            i -= 1
            j -= 1
        elif current == up + gap:
            align1 = seq1[i - 1] + align1
            align2 = "-" + align2
            i -= 1
        else:
            align1 = "-" + align1
            align2 = seq2[j - 1] + align2
            j -= 1

    while i > 0:
        align1 = seq1[i - 1] + align1
        align2 = "-" + align2
        i -= 1
    while j > 0:
        align1 = "-" + align1
        align2 = seq2[j - 1] + align2
        j -= 1

    match_line = get_match_line(align1, align2)
    identity = calculate_identity(align1, align2)
    return score_matrix[m][n], align1, align2, score_matrix, match_line, identity


def get_match_line(al1, al2):
    match_line = ""
    for a, b in zip(al1, al2):
        if a == b:
            match_line += "|"
        elif a == "-" or b == "-":
            match_line += " "
        else:
            match_line += "."
    return match_line


def calculate_identity(al1, al2):
    matches = 0
    length = len(al1)
    for a, b in zip(al1, al2):
        if a == b:
            matches += 1
    identity_percent = (matches / length) * 100
    return round(identity_percent, 2)
