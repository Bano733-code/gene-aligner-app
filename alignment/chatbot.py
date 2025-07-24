# alignment/chatbot.py

import os
import requests

# Make sure your GROQ_API_KEY is loaded securely (e.g., via Streamlit secrets or Colab form)
# and set in os.environ before calling this

def interpret_alignment(method, score, identity, align1, align2, question=None):
    try:
        # Clean and fetch key safely
        api_key = os.getenv("GROQ_API_KEY", "").strip()

        if not api_key:
            return "❌ Missing or invalid GROQ_API_KEY."

        # Construct prompt
        prompt = (
            f"You are a helpful bioinformatics expert.\n"
            f"Method: {method}\n"
            f"Score: {score}\n"
            f"Identity: {identity}%\n"
            f"Alignment 1: {align1}\n"
            f"Alignment 2: {align2}\n"
        )
        if question:
            prompt += f"User question: {question}\nAnswer concisely."

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "mixtral-8x7b-32768",
            "messages": [
                {"role": "system", "content": "You are a helpful bioinformatics expert."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 300
        }

        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        return f"❌ Exception occurred: {str(e)}"
