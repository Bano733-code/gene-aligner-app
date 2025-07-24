import os
import requests

def interpret_alignment(method, score, identity, align1, align2, question=None):
    """
    Sends alignment details to Groq API and returns the interpretation.

    Parameters:
        method (str): Alignment method used
        score (float or str): Alignment score
        identity (float or str): Identity percentage
        align1 (str): First aligned sequence
        align2 (str): Second aligned sequence
        question (str): Optional user question

    Returns:
        str: Chatbot response
    """
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        return "❌ Error: GROQ API key not set in environment."

    try:
        score = float(score)
        identity = float(identity)
    except ValueError:
        return "❌ Error: Score and Identity should be numeric."

    # Prompt to send
    prompt = (
        f"You are a bioinformatics expert. Analyze the following sequence alignment:\n"
        f"🔹 Method: {method}\n"
        f"🔸 Sequence 1: {align1}\n"
        f"🔸 Sequence 2: {align2}\n"
        f"📊 Score: {score}, Identity: {identity}%.\n"
    )

    if question:
        prompt += f"User question: {question}\n"

    prompt += "Explain the meaning of this result in simple terms."

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mixtral-8x7b-32768",
                "messages": [
                    {"role": "system", "content": "You are a helpful bioinformatics expert."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 500
            }
        )

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"❌ API Error {response.status_code}: {response.text}"

    except Exception as e:
        return f"❌ Exception occurred: {str(e)}"
