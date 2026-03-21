import time
import logging
import requests


class OllamaClient:
    BASE_URL = "http://localhost:11434/api/generate"
    DEFAULT_MODEL = "llama3.2:3b"

    def __init__(self, base_url=None, model=None):
        self.base_url = base_url or self.BASE_URL
        self.model = model or self.DEFAULT_MODEL

    def health_check(self, retries=3, delay=10):
        for attempt in range(retries):
            try:
                resp = requests.post(
                    self.base_url,
                    json={
                        "model": self.model,
                        "prompt": "ping",
                        "stream": False,
                        "options": {"num_predict": 1},
                    },
                    timeout=60,
                )
                resp.raise_for_status()
                data = resp.json()
                if "error" in data:
                    return False, data["error"]
                return True, None
            except requests.Timeout:
                if attempt < retries - 1:
                    time.sleep(delay)
                    continue
                return False, "Timeout waiting for Ollama server/model. Ensure model is loaded and try again."
            except Exception as e:
                return False, str(e)

    def generate(self, prompt, system=None, max_tokens=256, temperature=0.7):
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }
        if system:
            payload["system"] = system
        try:
            response = requests.post(self.base_url, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            if "error" in data:
                return f"[Ollama Error: {data['error']}]"
            if "response" in data:
                return data["response"].strip()
            return "[Error: Unexpected Ollama API response format]"
        except requests.Timeout:
            return "[Error: Ollama API timed out. Ensure model is loaded.]"
        except requests.RequestException as e:
            logging.error(f"Ollama API request error: {e}")
            return f"[Error: Unable to generate response: {e}]"
        except Exception as e:
            logging.error(f"Ollama API unexpected error: {e}")
            return f"[Error: Unexpected error: {e}]"
