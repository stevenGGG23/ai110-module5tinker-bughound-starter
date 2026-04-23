#!/usr/bin/env python3

from bughound_agent import BugHoundAgent
from llm_client import MockClient

def test_heuristic_mode():
    print("Testing Heuristic Mode (Offline)")
    agent = BugHoundAgent(client=None)  # No client = heuristic only
    code = """def greet(name):
    print("Hello", name)
    return True"""
    result = agent.run(code)

    print("Issues found:", len(result["issues"]))
    for issue in result["issues"]:
        print(f"- {issue['type']}: {issue['msg']}")

    print("Risk level:", result["risk"]["level"])
    print("Should auto-fix:", result["risk"]["should_autofix"])
    print("Fixed code preview:")
    print(result["fixed_code"][:200] + "..." if len(result["fixed_code"]) > 200 else result["fixed_code"])
    print()

def test_mock_llm_mode():
    print("Testing Mock LLM Mode (Simulates API)")
    agent = BugHoundAgent(client=MockClient())  # Mock client forces fallback
    code = """def load_data(path):
    try:
        data = open(path).read()
    except:
        return None
    return data"""
    result = agent.run(code)

    print("Issues found:", len(result["issues"]))
    for issue in result["issues"]:
        print(f"- {issue['type']}: {issue['msg']}")

    print("Risk level:", result["risk"]["level"])
    print("Should auto-fix:", result["risk"]["should_autofix"])
    print("Agent trace:")
    for log in result["logs"]:
        print(f"- {log['step']}: {log['message']}")
    print()

if __name__ == "__main__":
    test_heuristic_mode()
    test_mock_llm_mode()