"""Ollama API client."""

import requests


def check_ollama(url: str = "http://localhost:11434") -> bool:
    """Check if Ollama is running and reachable."""
    try:
        r = requests.get(f"{url}/api/tags", timeout=5)
        return r.status_code == 200
    except requests.RequestException:
        return False


def generate(prompt: str, model: str = "qwen3-coder", url: str = "http://localhost:11434") -> str:
    """Send a prompt to Ollama and return the generated text."""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.3,
            "num_predict": 4096,
        },
    }

    r = requests.post(f"{url}/api/generate", json=payload, timeout=120)
    r.raise_for_status()
    return r.json()["response"]
