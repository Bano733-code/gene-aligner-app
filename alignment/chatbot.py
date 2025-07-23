# alignment/chatbot.py

from transformers import pipeline

# Load Hugging Face model (Flan-T5)
generator = pipeline("text2text-generation", model="google/flan-t5-base")

def interpret_alignment(method, score, identity, align1, align2):
    if method == "Dot Matrix":
        return (
            "The Dot Matrix method provides a visual comparison of sequence similarity. "
            "Diagonal lines indicate regions of similarity or repeats, but this method "
            "does not generate alignment scores or identity percentages."
        )

    prompt = (
        f"Explain the gene sequence alignment using the {method} method.\n\n"
        f"Alignment 1:\n{align1}\n\n"
        f"Alignment 2:\n{align2}\n\n"
        f"Score: {score}\nIdentity: {identity}\n\n"
        f"Provide a short, research-level interpretation suitable for a bioinformatics professor."
    )

    try:
        result = generator(prompt, max_length=256, do_sample=False)
        return result[0]["generated_text"]
    except Exception as e:
        return f"⚠️ Error generating explanation: {e}"
