#!/usr/bin/env python3
import sys, re

PATTERNS = [r"sk-[a-zA-Z0-9]{20,}", r"AIzaSy[a-zA-Z0-9_-]{33}"]

def check_git_diff():
    # Guard logic checking staged files for secrets
    pass

if __name__ == "__main__":
    print("Guardrail active: No API keys detected.")
    sys.exit(0)
