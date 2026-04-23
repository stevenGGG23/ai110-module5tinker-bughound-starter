# BugHound Mini Model Card (Reflection)

Fill this out after you run BugHound in **both** modes (Heuristic and Gemini).

---

## 1) What is this system?

**Name:** BugHound  
**Purpose:** Analyze a Python snippet, propose a fix, and run reliability checks before suggesting whether the fix should be auto-applied.

**Intended users:** Students learning agentic workflows and AI reliability concepts.

---

## 2) How does it work?

The workflow is: PLAN → ANALYZE → ACT → TEST → REFLECT.

- PLAN: The agent logs that it's planning a quick scan and fix proposal.
- ANALYZE: Detect issues using heuristics (checks for print, bare except, TODO) or LLM (prompts for JSON array of issues).
- ACT: Propose fix using heuristics (replace bare except with specific exception, add logging for print) or LLM (rewrite code to address issues).
- TEST: Assess risk based on issue severity, structural changes, and syntax validity.
- REFLECT: Decide if safe to auto-fix based on risk level.

Heuristics handle simple rules offline, while Gemini provides more intelligent analysis and fixes when enabled.

---

## 3) Inputs and outputs

**Inputs:**

- Python code snippets, such as functions with print statements, try/except blocks, and TODO comments.
- Shape: Short scripts or functions, often with common issues like bare except or debug prints.

**Outputs:**

- Issues: Lists of detected problems with type (e.g., Code Quality, Reliability), severity (Low/Medium/High), and message.
- Fixes: Rewritten code addressing issues, like replacing print with logging or specifying exceptions.
- Risk report: Score (0-100), level (low/medium/high), reasons for deductions, and whether to auto-fix.

---

## 4) Reliability and safety rules

1. **High severity issue deduction (-40 score):** Checks if any detected issue is marked high severity. Matters for safety as high severity issues like bare except can cause silent failures. False positive: Overly cautious if the issue isn't critical in context. False negative: If a medium severity issue is actually high risk.

2. **Fixed code much shorter (-20 score):** Checks if fixed code is less than 50% of original lines. Matters to prevent accidental code removal. False positive: If shortening is intentional and correct. False negative: If lengthening code is problematic.

---

## 5) Observed failure modes

1. **Missed issue:** Heuristics might not detect nuanced issues like improper error handling beyond bare except, or logic errors not covered by simple rules.

2. **Risky fix:** Heuristic fix replaces print with logging but doesn't configure the logger, potentially causing runtime errors if logging isn't set up. LLM might over-edit code, changing behavior unintentionally.

---

## 6) Heuristic vs Gemini comparison

- Gemini detects more varied issues beyond the hardcoded heuristics, like readability or logic problems.
- Heuristics consistently catch known patterns like print and bare except.
- Fixes: Gemini proposes more comprehensive changes, heuristics make minimal replacements.
- Risk scorer aligns with intuition for obvious issues but may not catch subtle behavior changes.

---

## 7) Human-in-the-loop decision

Scenario: When risk level is medium, refuse auto-fix.

- Trigger: If risk["level"] == "medium", set should_autofix = False.
- Implement in risk_assessor.py, in the auto-fix policy section.
- Message: "Fix is moderately risky. Human review recommended."

---

## 8) Improvement idea

Add syntax validation in risk assessment: Check if fixed code parses correctly with ast.parse. If not, heavily penalize score to prevent auto-fixing broken code. This catches LLM errors without complex parsing.
