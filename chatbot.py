import json
import os
import sys
from utils.ollama_client import OllamaClient
from utils.prompt_loader import PromptLoader
from utils.logger import Logger

PROMPTS_DIR = "prompts"
DATA_PATH = "data/queries.json"
RESULTS_PATH = "eval/results.md"

METHODS = [
    ("Zero-Shot", "zero_shot_template.txt"),
    ("One-Shot", "one_shot_template.txt"),
]

RESULTS_HEADER = (
    "# Chatbot Evaluation Results\n\n"
    "## Scoring Rubric\n\n"
    "| Score | Relevance | Coherence | Helpfulness |\n"
    "|-------|-----------|-----------|-------------|\n"
    "| 5 | Directly answers all aspects | Perfectly clear and logical | Fully actionable, solves the problem |\n"
    "| 4 | Mostly relevant, minor gaps | Mostly clear, minor confusion | Helpful, but could be improved |\n"
    "| 3 | Partially relevant, some missing info | Somewhat clear, some awkwardness | Somewhat helpful |\n"
    "| 2 | Barely relevant | Hard to follow | Little help |\n"
    "| 1 | Not relevant | Incoherent | Not helpful |\n\n"
    "---\n\n"
    "## Evaluation Table\n\n"
    "| Query # | Customer Query | Prompting Method | Response | Relevance (1-5) | Coherence (1-5) | Helpfulness (1-5) |\n"
    "|---------|---------------|------------------|----------|-----------------|-----------------|-------------------|\n"
)


def check_ollama_ready(client):
    print("[INFO] Checking Ollama server connectivity...")
    ok, err = client.health_check()
    if not ok:
        print(f"[FATAL] Ollama server/model not available: {err}")
        sys.exit(1)
    print("[INFO] Ollama server is ready.")


def load_queries(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            queries = json.load(f)
        print(f"[INFO] Loaded {len(queries)} queries from {path}")
        return queries
    except FileNotFoundError:
        print(f"[FATAL] Query file not found: {path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"[FATAL] Invalid JSON in {path}: {e}")
        sys.exit(1)


def sanitize_for_table(text):
    cleaned = text.replace("\n", " ").replace("\r", " ").replace("|", "\\|")
    return " ".join(cleaned.split())


def write_results(results, path):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(RESULTS_HEADER)
            for r in results:
                response = sanitize_for_table(r["response"])
                f.write(
                    f"| {r['query_num']} "
                    f"| {r['customer_query']} "
                    f"| {r['method']} "
                    f"| {response} "
                    f"|   |   |   |\n"
                )
            f.write("\n---\n\n")
            f.write("## Average Scores\n\n")
            f.write("| Prompting Method | Avg. Relevance | Avg. Coherence | Avg. Helpfulness |\n")
            f.write("|------------------|---------------|----------------|------------------|\n")
            f.write("| Zero-Shot        |               |                |                  |\n")
            f.write("| One-Shot         |               |                |                  |\n")
        print(f"[INFO] Results written to {path}")
    except Exception as e:
        print(f"[FATAL] Failed to write results: {e}")
        sys.exit(1)


def main():
    logger = Logger()
    prompt_loader = PromptLoader(PROMPTS_DIR)
    client = OllamaClient()

    check_ollama_ready(client)
    queries = load_queries(DATA_PATH)
    system_context = prompt_loader.load("system_context.txt")

    total = len(queries) * len(METHODS)
    results = []
    query_num = 1

    for q in queries:
        for method, template_file in METHODS:
            template = prompt_loader.load(template_file)
            prompt = prompt_loader.render(template, {
                "system_context": system_context,
                "customer_query": q["query"],
            })

            progress = len(results) + 1
            print(f"[{progress}/{total}] Q{query_num} [{method}]: {q['query'][:60]}...")

            logger.info(f"[Q{query_num}][{method}] Query: {q['query']}")
            response = client.generate(prompt, system=system_context)
            logger.info(f"[Q{query_num}][{method}] Response: {response}")

            results.append({
                "query_num": query_num,
                "customer_query": q["query"],
                "method": method,
                "response": response.strip(),
            })

        query_num += 1

    write_results(results, RESULTS_PATH)
    print(f"\n[DONE] Processed {len(results)} responses. See {RESULTS_PATH}")


if __name__ == "__main__":
    main()
