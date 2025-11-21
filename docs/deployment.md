# Deployment Guide

This guide outlines the recommended procedure for packaging and deploying Prompt Shield.

## 1. Prepare the environment

    ```bash
     python -m venv .venv
     .venv\Scripts\activate        # On Mac/Linux use: source .venv/bin/activate
     pip install --upgrade pip
     pip install -e .
     pip install build twine
    ```

## 2. Run quality gates

**It is good practice to run static analysis and tests before shipping:**

    ```bash
    pytest -q
    ```
*Add tooling such as Ruff or Black if your team enforces style checks.*

## 3. Build distribution artifacts

    ```bash
    python -m build
    ```
*This produces wheel (.whl) and source (.tar.gz) archives in dist/.*

## 4. Verify artifacts locally

**Install the freshly built wheel into a clean environment:**

    ```bash
    pip install dist/Prompt_Shield-1.0.0-py3-none-any.whl
    Prompt_Shield --text 'Sanity check run'
    ```

## 5. Publish to PyPI (or an internal index)

    ```bash
    twine upload dist/*
    ```
Use --repository-url for private indexes as needed.

## 6. Runtime configuration

**Ensure the following variables are set in your runtime (CI/CD, container, serverless, etc.):**

- PROMPT_SHIELD_HIGH_RISK_TERMS
- PROMPT_SHIELD_MEDIUM_RISK_TERMS
- PROMPT_SHIELD_MAX_PROMPT_LENGTH
