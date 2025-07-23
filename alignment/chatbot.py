from openai import OpenAI
import streamlit as st

# Create OpenAI client using your secret API key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def interpret_alignment(method, score, identity, align1, align2):
    prompt = f"""
You are a helpful bioinformatics assistant.

A user performed a {method} alignment between two gene sequences.

Here are the results:

🔹 Alignment Score: {score}
🔹 Identity: {identity:.2f}%

🧬 Aligned Sequence 1:
{align1}

🧬 Aligned Sequence 2:
{align2}

Can you explain what these results mean in simple terms?
Provide a short summary of the alignment quality and whether it indicates strong similarity between the sequences.
"""

    # Use OpenAI Chat API (new v1.x SDK format)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if you have access
        messages=[
            {"role": "system", "content": "You are a helpful bioinformatics assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=500
    )

    return response.choices[0].message.content
