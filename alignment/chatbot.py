# utils/chatbot.py
def interpret_alignment(method, score, identity, align1, align2):
    if method == "Dot Matrix":
        return "The dot matrix visually compares two sequences. Diagonal lines suggest regions of similarity or repeats."

    elif method == "Needleman-Wunsch":
        return (
            f"Global alignment completed using Needleman-Wunsch.\n\n"
            f"🧮 Score: {score}\n"
            f"🔗 Identity: {identity:.2f}%\n\n"
            "This method aligns from start to end. High score and identity suggest strong global similarity."
        )

    elif method == "Smith-Waterman":
        return (
            f"Local alignment completed using Smith-Waterman.\n\n"
            f"🧮 Score: {score}\n"
            f"🔗 Identity: {identity:.2f}%\n\n"
            "This method finds the best matching region within the two sequences."
        )

    elif method == "Word Method":
        return (
            "Word method looks for short identical or similar words. "
            "It's a heuristic method and good for quick comparisons, not for full alignment."
        )

    else:
        return "No interpretation available for the selected method."
