# alignment/chatbot.py

import replicate
import os

# Ensure your API token is loaded
os.environ["REPLICATE_API_TOKEN"] = os.getenv("REPLICATE_API_TOKEN")

def interpret_alignment(method, score, identity, align1, align2, question=None):
    if not os.getenv("REPLICATE_API_TOKEN"):
        return "🚫 Replicate API token not set. Please set it in Streamlit Secrets."

    # Compose the prompt
    prompt = (
        f"You are a bioinformatics expert. Based on the {method} alignment:\n"
        f"Alignment 1: {align1}\nAlignment 2: {align2}\n"
        f"Score: {score}, Identity: {identity}.\n"
    )
    if question:
        prompt += f"User question: {question}\nAnswer concisely."

    try:
        output = replicate.run(
            "mistralai/mistral-7b-instruct-v0.1",
            input={"prompt": prompt, "max_new_tokens": 300}
        )
        return "".join(output)
    except Exception as e:
        return f"❌ Error: {e}"
