import numpy as np

def smith_waterman(seq1, seq2, match=2, mismatch=-1, gap=-2):
    m, n = len(seq1), len(seq2)
    matrix = np.zeros((m + 1, n + 1), dtype=int)

    max_score = 0
    max_pos = (0, 0)

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match_score = match if seq1[i - 1] == seq2[j - 1] else mismatch
            score = max(
                0,
                matrix[i - 1][j - 1] + match_score,
                matrix[i - 1][j] + gap,
                matrix[i][j - 1] + gap
            )
            matrix[i][j] = score
            if score > max_score:
                max_score = score
                max_pos = (i, j)

    align1, align2 = "", ""
    i, j = max_pos
    while i > 0 and j > 0 and matrix[i][j] != 0:
        score = matrix[i][j]
        diag = matrix[i - 1][j - 1]
        up = matrix[i - 1][j]
        left = matrix[i][j - 1]

        match_score = match if seq1[i - 1] == seq2[j - 1] else mismatch
        if score == diag + match_score:
            align1 = seq1[i - 1] + align1
            align2 = seq2[j - 1] + align2
            i -= 1
            j -= 1
        elif score == up + gap:
            align1 = seq1[i - 1] + align1
            align2 = "-" + align2
            i -= 1
        else:
            align1 = "-" + align1
            align2 = seq2[j - 1] + align2
            j -= 1

    match_line = get_match_line(align1, align2)
    identity = calculate_identity(align1, align2)
    return max_score, align1, align2, matrix, match_line, identity


def get_match_line(al1, al2):
    return "".join(["|" if a == b else "." if a != "-" and b != "-" else " " for a, b in zip(al1, al2)])

def calculate_identity(al1, al2):
    matches = sum(a == b for a, b in zip(al1, al2))
    return round((matches / len(al1)) * 100, 2)
