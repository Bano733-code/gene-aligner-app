# alignment/chatbot.py

from transformers import pipeline

# Load free Hugging Face model (can switch to 'flan-t5-large' if needed)
generator = pipeline("text2text-generation", model="google/flan-t5-base")

def interpret_alignment(method, score, identity, align1, align2, question=None):
    # Optional: Prevent overload from very long alignments
    max_length = 150
    if len(align1) > max_length:
        align1 = align1[:max_length] + "..."
    if len(align2) > max_length:
        align2 = align2[:max_length] + "..."

    # Handle perfect match
    if align1 == align2:
        return "✅ Both aligned sequences are identical. This suggests a perfect alignment with no gaps or mismatches."

    # Prompt when a question is asked
    if question:
        prompt = (
            f"You are a bioinformatics expert. Based on the following {method} alignment result:\n\n"
            f"Score: {score}\nIdentity: {identity}%\n"
            f"Sequence 1: {align1}\nSequence 2: {align2}\n\n"
            f"User question: {question}\n\n"
            f"Give a concise and informative answer suitable for a genetics researcher. Avoid repeating identical phrases."
        )
    else:
        # Prompt when no specific question
        prompt = (
            f"You are a bioinformatics expert. Interpret the following {method} alignment result:\n\n"
            f"Score: {score}\nIdentity: {identity}%\n"
            f"Sequence 1: {align1}\nSequence 2: {align2}\n\n"
            f"Explain whether the alignment is good, highlight any gaps or mismatches, "
            f"and describe the biological meaning in a research-grade tone. Avoid repetition."
        )

    result = generator(prompt, max_new_tokens=256, do_sample=False)
    return result[0]["generated_text"]
