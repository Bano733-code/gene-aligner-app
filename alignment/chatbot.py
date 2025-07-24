import os
import requests

api_key = os.getenv("GROQ_API_KEY", "").strip()

res = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    json={
        "model": "mixtral-8x7b-32768",
        "messages": [{"role": "user", "content": "Say hello"}],
        "temperature": 0.5,
        "max_tokens": 50
    }
)

print(res.status_code, res.text)
