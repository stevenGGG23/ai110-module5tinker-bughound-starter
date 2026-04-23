# BugHound

BugHound is a small, agent-style debugging tool. It analyzes a Python code snippet, proposes a fix, and runs basic reliability checks before deciding whether the fix is safe to apply automatically.

---

## What BugHound Does

Given a short Python snippet, BugHound:

1. **Analyzes** the code for potential issues  
   - Uses heuristics in offline mode (detects print statements, bare except blocks, TODO comments)  
   - Uses Gemini when API access is enabled (expects structured JSON output)  
   - Validates LLM responses for format compliance; falls back to heuristics if invalid  

2. **Proposes a fix**  
   - Heuristic-based: minimal changes like replacing print with logging or specifying exceptions  
   - LLM-generated: comprehensive rewrites preserving behavior  
   - Strips code fences and validates output  

3. **Assesses risk**  
   - Scores based on issue severity, structural changes, code length, and syntax validity  
   - Penalizes high-severity issues, missing returns, excessive shortening/lengthening, and syntax errors  
   - Decides auto-fix only for low-risk changes  

4. **Shows its work**  
   - Displays detected issues with type, severity, and description  
   - Shows a unified diff between original and fixed code  
   - Logs each agent step (PLAN → ANALYZE → ACT → TEST → REFLECT)  
   - Provides risk report with score, level, reasons, and auto-fix recommendation  

---

## Demo Screenshot

Here's what BugHound looks like in action:

![BugHound Demo](Screenshot%202026-04-22%20at%209.18.27%E2%80%AFPM.png)

---

## Reliability Features

BugHound includes multiple guardrails to prevent unsafe AI behavior:

- **Fallback Logic**: If LLM output is malformed or contains extra text, automatically uses heuristics
- **Syntax Validation**: Rejects fixes with syntax errors (prevents applying broken code)
- **Conservative Risk Scoring**: Penalizes changes that alter structure, remove returns, or significantly change length
- **Testing**: Comprehensive tests ensure fallbacks work and guardrails trigger appropriately

---

## Setup

### 1. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
# or
venv\Scripts\activate      # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running in Offline (Heuristic) Mode

No API key required.

```bash
streamlit run bughound_app.py
```

In the sidebar, select:

* **Model mode:** Heuristic only (no API)

This mode uses simple pattern-based rules and is useful for testing the workflow without network access.

---

## Running with Gemini

### 1. Set up your API key

Copy the example file:

```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:

```text
GEMINI_API_KEY=your_real_key_here
```

### 2. Run the app

```bash
streamlit run bughound_app.py
```

In the sidebar, select:

* **Model mode:** Gemini (requires API key)
* Choose a Gemini model and temperature

BugHound will now use Gemini for analysis and fix generation, while still applying local reliability checks.

---

## Running Tests

Tests focus on **reliability logic** and **agent behavior**, not the UI.

```bash
python -m pytest tests/
```

You should see tests covering:

* Risk scoring and guardrails (including syntax validation)
* Heuristic fallbacks when LLM output is invalid
* End-to-end agent workflow shape

### Quick Functional Test

Run the included test script to see BugHound in action:

```bash
python test_bughound.py
```

This demonstrates heuristic and mock LLM modes without the UI.

---

## Model Card

See `model_card.md` for a detailed analysis of BugHound's capabilities, limitations, failure modes, and safety rules.
