import openai
import streamlit as st

# Securely load API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

def interpret_alignment(method, score, identity, align1, align2):
    prompt = f"""You're a bioinformatics assistant. Explain the following {method} alignment between two sequences.
    
Alignment Score: {score}
Sequence Identity: {identity}%
Aligned Sequences:
{align1}
{align2}

Explain this alignment's significance in simple terms for a student."""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if you have access
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=400
    )
    
    return response["choices"][0]["message"]["content"]
