# Intent: Receipt-to-Data Vision Processor & Checker

## Purpose
A Python script that uses vision-capable LLMs to extract structured transaction data from receipt images, validates line items against arithmetic calculations via a custom checker, and enforces security via local guardrail hooks.

## Target Audience
Automated expense reporting and receipt digitization workflows.

## Core Commitments
1. Extract receipt fields (date, vendor, line items, total) into valid JSON.
2. The checker component must independently verify math rather than blindly trusting the model.
3. Security guardrail hook installed to prevent API key leaks.

## Approved by
Jeevan Gowda Kumaraswamy
Date: October 26, 2026
