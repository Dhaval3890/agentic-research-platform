import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

def ollama_call(prompt: str, model="phi3:mini", temperature=0.2):
    payload = {
        "model": model,
        "prompt": prompt,
        "temperature": temperature,
        "stream": True   # 🔥 THIS IS THE FIX
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        stream=True      # 🔥 THIS IS THE FIX
    )

    full_text = ""

    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))
            full_text += data.get("response", "")

    return full_text.strip()
