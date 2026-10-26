import os
import json
from parser import parse_receipt_image
from checker import validate_receipt

def run_eval():
    models = ["anthropic/claude-3.5-haiku", "openai/gpt-4o-mini"]
    print("=== Week 5 Receipt Vision & Checker Evaluation ===")
    
    # Placeholder run structure for evaluation matrix
    for model in models:
        print(f"Evaluating Model: {model}")
        print("-" * 50)

if __name__ == "__main__":
    run_eval()
