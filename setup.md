# Setup Guide: Offline Customer Support Chatbot

## System Requirements
- **OS**: Windows 10/11, macOS 12+, or Linux (Ubuntu 20.04+)
- **RAM**: Minimum 8 GB (16 GB recommended for smooth inference)
- **Disk**: ~2 GB free space for the Llama 3.2 3B model
- **Python**: 3.9 or higher
- **GPU**: Optional (CPU inference works, GPU accelerates it)

## 1. Install Ollama

Download and install Ollama from the official website:

- **Website**: [https://ollama.com/download](https://ollama.com/download)
- Follow the platform-specific installer instructions
- After installation, verify it works:
  ```bash
  ollama --version
  ```

## 2. Download the Llama 3.2 3B Model

Open a terminal and run:

```bash
ollama pull llama3.2:3b
```

This downloads the ~2 GB model. Wait for it to complete. You can verify it's available:

```bash
ollama list
```

You should see `llama3.2:3b` in the output.

## 3. Set Up Python Environment

Create and activate a virtual environment:

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 4. Start the Ollama Server

If Ollama isn't already running, start it:

```bash
ollama serve
```

On most systems, Ollama runs automatically as a background service after installation. You can skip this step if you see a "port already in use" message.

## 5. Run the Chatbot

```bash
python chatbot.py
```

The script will:
1. Check that Ollama and the model are available
2. Load 20 customer queries from `data/queries.json`
3. Generate responses using both zero-shot and one-shot prompting
4. Save results to `eval/results.md`
5. Log all activity to `logs/`

You'll see progress output like:
```
[INFO] Checking Ollama server connectivity...
[INFO] Ollama server is ready.
[INFO] Loaded 20 queries from data/queries.json
[1/40] Q1 [Zero-Shot]: Where is my order? It was supposed to arrive yester...
[2/40] Q1 [One-Shot]: Where is my order? It was supposed to arrive yester...
...
[DONE] Processed 40 responses. See eval/results.md
```

## 6. Evaluate Responses

Open `eval/results.md` and manually score each response using the rubric provided at the top of the file. Calculate averages for zero-shot and one-shot methods.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `[FATAL] Ollama server/model not available` | Make sure Ollama is running (`ollama serve`) and the model is downloaded (`ollama list`) |
| `Timeout waiting for Ollama` | The model may be loading for the first time. Wait a few minutes and try again |
| `ModuleNotFoundError: requests` | Activate your virtual environment and run `pip install -r requirements.txt` |
| Empty or error responses | Check `logs/` directory for detailed error messages |
| `FileNotFoundError: Prompt template` | Ensure the `prompts/` directory contains all three template files |
