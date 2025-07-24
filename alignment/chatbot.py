# alignment/chatbot.py

from transformers import pipeline

# Load free Hugging Face model
generator = pipeline("text2text-generation", model="google/flan-t5-base")

def interpret_alignment(method, score, identity, align1, align2, question=None):
    if question:
        prompt = (
            f"You are a bioinformatics expert. Based on the {method} alignment:\n"
            f"Alignment 1: {align1}\nAlignment 2: {align2}\n"
            f"Score: {score}, Identity: {identity}.\n"
            f"User question: {question}\n"
            f"Answer the question concisely and professionally."
        )
    else:
        prompt = (
            f"Explain the following gene sequence alignment using {method}:\n\n"
            f"Alignment 1: {align1}\nAlignment 2: {align2}\n"
            f"Score: {score}\nIdentity: {identity}\n\n"
            "Provide a brief, research-grade interpretation suitable for a bioinformatics professor."
        )

    result = generator(prompt, max_length=256, do_sample=False)
    return result[0]["generated_text"]
