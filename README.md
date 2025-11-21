# Prompt Shield

## Overview 👩‍💻

Prompt Shield is a CLI-first prompt risk linter designed to intercept sensitive or policy-violating input before it reaches an LLM. It inspects prompts for personally identifiable information (PII), configurable risky terminology, and oversized payloads, surfacing well-structured findings with contextual snippets and a cumulative risk score.

---

## Features ✅

- 🔍 **PII detection** for emails, phone numbers, IPv4 addresses, SSNs, and credit cards.
- ⚠️ **Configurable term scanning** for both high-risk and cautionary (medium-risk) keywords.
- 📏 **Prompt length enforcement** with severity that scales with the overage.
- 🧠 **Deterministic risk scoring** that maps findings to low/medium/high labels.
- 🖥️ **Human or machine-friendly output** via plain text or JSON formats.
- ⚙️ **Environment-driven configuration** to align with organisational policies.

---

## Requirements 💻

- Python **3.10+**
- `pip` for dependency management

---

## Project Structure 📁

    ```
     Prompt_Shield/
     ├── cli/
     │   └── __init__.py
     |   ├── cli.py
     ├── utils/
     │   └── __init__.py
     |   ├── utils.py
     ├── config/
     │   └── __init__.py
     |   ├── config.py
     ├── tests/
     │   └── test_analyser.py
     ├── .env
     ├── __init__.py
     ├── __main__.py
     ├── analyser.py
     ├── detectors.py
     ├── main.py
     ├── pyproject.toml
     └── README.md
    ```
---

## Installation 🛠️

    ```bash
     git clone https://github.com/Suiper34/Prompt_Shield.git
     cd Prompt_Shield
     python -m venv .venv
     .venv\Scripts\activate        # On Mac/Linux use: source .venv/bin/activate
     pip install --upgrade pip
     pip install -e .
    ```

---

## Configuration ⚙️

Prompt Shield reads its settings from environment variables (with sensible defaults):

**Variable**                          |      **Default**                              |         **Description**
`PROMPT_SHIELD_HIGH_RISK_TERMS`       |  *api_key,ssh_key,trade_secret,customer_ssn*  | *Comma-separated list of critical terms that should immediately trigger high risk.*
`PROMPT_SHIELD_MEDIUM_RISK_TERMS`     |   *password,internal_only,confidential*       | *Comma-separated list of cautionary terms.*
`PROMPT_SHIELD_MAX_PROMPT_LENGTH`     |   *1500*                                      | *Maximum allowed character length for a prompt.*

- *You can export them, place them in a .env, or configure them in your deployment platform.*

---

## Usage 🧩

- Analyse inline text:

        ```bash
        Prompt_Shield --text 'Please email the draft contract to jane.doe@example.com.'
        ```

- Analyse a file:

        ```bash
        Prompt_Shield --file ./samples/prompt.txt
        ```
- Pipe from stdin:

        ```bash
        cat samples/prompt.txt | Prompt_Shield
        ```

- Request JSON output (ideal for automation):

        ```bash
        Prompt_Shield --text 'Share the api_key with the vendor.' --format json
        ```

- Enable verbose logging for debugging:

        ```bash
        Prompt_Shield --text '...' --verbose
        ```

---

## Testing 🧪

Run the automated test suite with:

    ```bash
    pytest -q
    ```
---

## Deployment 🚀

For deployment instructions, refer to the [`docs/deployment.md`](./docs/deployment.md) file.

---

## License 📜

This project is released under the JhapTech Permissive License [`see LICENSE`](./LICENSE). TL;DR: you may use, modify, and redistribute with attribution.

---

Made with ❤️ by Jhaptech. Illuminate and iterate✨
