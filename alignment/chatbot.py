import replicate
import os

# Load your Replicate token (make sure you set it as a secret)
os.environ["REPLICATE_API_TOKEN"] = "your_replicate_api_key"

def interpret_alignment(method, score, identity, align1, align2, question=None):
    prompt = (
        f"You are a bioinformatics expert. Based on the {method} alignment:\n"
        f"Alignment 1: {align1}\nAlignment 2: {align2}\n"
        f"Score: {score}, Identity: {identity}.\n"
    )
    if question:
        prompt += f"User question: {question}\nAnswer concisely."

    output = replicate.run(
        "mistralai/mistral-7b-instruct-v0.1",
        input={"prompt": prompt, "max_new_tokens": 300}
    )

    return "".join(output)
