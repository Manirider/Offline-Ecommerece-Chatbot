# Offline Customer Support Chatbot - Chic Boutique

A production-grade, fully offline AI-powered customer support chatbot built with Python, Ollama, and Llama 3.2. Delivers human-like, privacy-first support with zero cloud dependencies.

## Project Overview

This project implements an offline customer support chatbot for the fictional e-commerce store **Chic Boutique**. It uses Meta's **Llama 3.2 3B** model served locally via **Ollama** to generate warm, professional, and actionable customer support responses entirely offline.

The project demonstrates:
- Prompt engineering techniques (zero-shot vs one-shot) and their impact on response quality
- Manual evaluation methodology with a structured scoring rubric
- Privacy-first architecture suitable for GDPR/DPDP compliance


## Features

| Feature | Description |
|---------|-------------|
| Fully Offline | No internet, cloud APIs, or external services required |
| Llama 3.2 3B | Lightweight yet capable local LLM via Ollama |
| Human-Like Responses | Warm, empathetic, concise, and actionable support |
| Prompt Engineering | Zero-shot vs one-shot comparison with 20 diverse queries |
| Evaluation System | Structured scoring on relevance, coherence, and helpfulness |
| Modular Architecture | Clean separation of concerns across focused modules |
| Privacy by Design | All data stays on your machine (GDPR/DPDP ready) |
| Comprehensive Logging | Timestamped logs for every query and response |

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.9+ |
| LLM Server | Ollama (local inference) |
| Model | Llama 3.2 3B (Meta) |
| HTTP Client | requests |
| Data Format | JSON (queries), Markdown (results, report) |
| Logging | Python logging (file-based) |

## Architecture

```
offline-ecommerce-chatbot/
├── chatbot.py                 <- Main orchestrator
├── utils/
│   ├── __init__.py
│   ├── ollama_client.py       <- Ollama API communication
│   ├── prompt_loader.py       <- Template loading & rendering
│   └── logger.py              <- File-based logging
├── prompts/
│   ├── system_context.txt     <- Persona & rules
│   ├── zero_shot_template.txt <- Zero-shot prompt template
│   └── one_shot_template.txt  <- One-shot prompt template
├── data/
│   └── queries.json           <- 20 customer queries (5 categories)
├── eval/
│   └── results.md             <- Evaluation results & scores
├── logs/                      <- Auto-generated log files
├── report.md                  <- Performance analysis report
├── setup.md                   <- Installation guide
├── requirements.txt           <- Python dependencies
└── README.md
```

**Data Flow:**
1. `chatbot.py` loads queries from `data/queries.json`
2. For each query, it renders both zero-shot and one-shot prompts via `prompt_loader.py`
3. Prompts are sent to Ollama's local API via `ollama_client.py`
4. Responses are logged via `logger.py` and written to `eval/results.md`

## Prompt Engineering

### System Context
Defines a strict persona with rules:
- No hallucination - if unsure, ask for clarification
- Concise responses (2-4 sentences)
- Warm, empathetic tone with phrases like "Happy to help!"
- No AI self-references
- Step-by-step guidance where applicable

### Zero-Shot Prompting
Provides only the system context and customer query. Tests the model's baseline ability to generate appropriate support responses without any demonstration.

### One-Shot Prompting
Adds a single high-quality example response to anchor the model's style, tone, and structure. The example covers a "wrong item received" scenario and demonstrates the expected response format.

**Key insight:** The single example dramatically improves consistency - one-shot responses scored **5.00/5** vs zero-shot's **4.32/5** across all metrics.

## Evaluation Summary

20 customer queries x 2 prompting methods = **40 evaluated responses**

| Prompting Method | Avg. Relevance | Avg. Coherence | Avg. Helpfulness | Overall |
|------------------|---------------|----------------|------------------|---------|
| Zero-Shot        | 4.15          | 4.75           | 4.05             | 4.32    |
| One-Shot         | 5.00          | 5.00           | 5.00             | 5.00    |

See [eval/results.md](eval/results.md) for individual scores and [report.md](report.md) for deep analysis.

## Key Insights

1. **One-shot > Zero-shot**: A single example boosts all metrics by +0.68 points on average, especially helpfulness (+0.95)
2. **Tone anchoring**: The example response acts as a style guide, producing consistently warm and professional outputs
3. **Llama 3.2 3B capability**: Even a 3B model can deliver production-quality support responses with proper prompt engineering
4. **Privacy advantage**: Fully local inference eliminates data privacy concerns without sacrificing quality
5. **Soft hallucination risk**: Zero-shot responses tend toward vague hedging; one-shot prompting reduces this


## Future Improvements

- **RAG Integration** - Connect to a policy/FAQ knowledge base for factually grounded responses
- **Database Connectivity** - Enable real-time order, payment, and account lookups
- **Multi-Turn Memory** - Support conversation history for follow-up queries
- **Web UI** - Build a user-friendly chat interface
- **Automated Evaluation** - LLM-as-judge scoring for reproducible metrics
- **Model Scaling** - Evaluate Llama 3.2 7B or fine-tuned variants


## Quick Start

```bash
# Install Ollama from https://ollama.com/download

# Download the model
ollama pull llama3.2:3b

# Set up Python environment
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Run the chatbot
python chatbot.py
```

See [setup.md](setup.md) for detailed instructions.


## Author 

MANIKANTA SURYASAI 
AIML ENGINEER | DEVELOPER
