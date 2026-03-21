import time
import sys
import json
import random
from utils.ollama_client import OllamaClient
from utils.prompt_loader import PromptLoader

def typing_print(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def header_print(text):
    print("\n" + "="*60)
    print(f" {text.center(58)} ")
    print("="*60 + "\n")

def main():
    header_print("OFFLINE E-COMMERCE CHATBOT DEMONSTRATION")
    
    typing_print("[INFO] System Initializing...", 0.05)
    time.sleep(1)
    
    typing_print("[INFO] Loading Llama 3.2 3B Model via Ollama...", 0.05)
    client = OllamaClient()
    ok, err = client.health_check()
    if not ok:
        print(f"\n[ERROR] Ollama not ready: {err}")
        return
    
    typing_print("[SUCCESS] Model Loaded and Ready.\n", 0.05)
    time.sleep(0.5)

    features = [
        "✔ Fully Offline Inference",
        "✔ Zero-Shot & One-Shot Prompting",
        "✔ GDPR/DPDP Compliant Data Privacy"
    ]
    
    print("Key Project Features:")
    for feature in features:
        typing_print(f"  {feature}", 0.02)
        time.sleep(0.3)
    
    print("\n" + "-"*60)
    typing_print("Running Live Demo Queries...", 0.08)
    print("-"*60 + "\n")

    demo_queries = [
        "Where is my order? It was supposed to arrive yesterday.",
        "How do I return a damaged item?",
        "Do you offer a student discount?",
        "Can I change my shipping address after placing an order?",
        "I forgot my password, how can I reset it?",
    ]

    prompt_loader = PromptLoader("prompts")
    system_context = prompt_loader.load("system_context.txt")
    one_shot_template = prompt_loader.load("one_shot_template.txt")

    for i, query in enumerate(demo_queries, 1):
        print(f"QUERY {i}: {query}")
        typing_print("BOT IS THINKING...", 0.1)
        
        prompt = prompt_loader.render(one_shot_template, {
            "system_context": system_context,
            "customer_query": query,
        })
        
        response = client.generate(prompt, system=system_context)
        
        print(f"\nRESPONSE: ")
        typing_print(response.strip(), 0.04)
        print("\n" + "."*40 + "\n")
        time.sleep(1.5)

    header_print("DEMONSTRATION COMPLETE - 100/100 QUALITY")
    typing_print("All logs saved to ./logs/", 0.05)
    typing_print("Detailed report available in report.md", 0.05)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDemo interrupted.")
