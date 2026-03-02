#!/usr/bin/env python3
"""
Test harness for sprint_agent.py
Executes a few stories and verifies telemetry collection.
"""

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
SCRIPTS_DIR = REPO_ROOT / ".github" / "scripts"

def run_sprint_agent(sprint_id="S05", limit=3) -> int:
    """Run sprint_agent with test mode."""
    
    print("=" * 70)
    print(f"SPRINT AGENT TEST: {sprint_id} (limit={limit} stories)")
    print("=" * 70)
    print()
    
    cmd = [
        "python",
        str(SCRIPTS_DIR / "sprint_agent.py"),
        "--issue", "1001",
        "--repo", "eva-foundry/53-refactor",
        "--sprint", sprint_id,
        "--stories-limit", str(limit),
        "--test-mode"
    ]
    
    result = subprocess.run(cmd, cwd=str(REPO_ROOT))
    return result.returncode


def verify_telemetry():
    """Verify telemetry files were created."""
    
    print("\n" + "=" * 70)
    print("TELEMETRY VERIFICATION")
    print("=" * 70)
    print()
    
    # Check .eva/sprints/ directory
    sprints_dir = REPO_ROOT / ".eva" / "sprints"
    if not sprints_dir.exists():
        print(f"[WARN] {sprints_dir} does not exist")
        return False
    
    context_files = list(sprints_dir.glob("SPRINT-*-context.json"))
    if not context_files:
        print(f"[WARN] No context files found in {sprints_dir}")
        return False
    
    print(f"[PASS] Found {len(context_files)} context file(s)")
    
    for ctx_file in sorted(context_files)[-1:]:  # Check latest
        print(f"\n[INFO] Analyzing: {ctx_file.name}")
        
        try:
            ctx_data = json.loads(ctx_file.read_text())
            
            print(f"  Correlation ID: {ctx_data.get('correlation_id')}")
            print(f"  Sprint ID: {ctx_data.get('sprint_id')}")
            
            metrics = ctx_data.get("metrics", {})
            print(f"\n  Metrics:")
            print(f"    - Total Stories: {metrics.get('total_stories', 0)}")
            print(f"    - Stories Done: {metrics.get('stories_done', 0)}")
            print(f"    - LM Calls: {metrics.get('lm_calls', 0)}")
            print(f"    - Total Tokens: {metrics.get('total_tokens', 0)}")
            print(f"    - Total Cost: ${metrics.get('total_cost_usd', 0):.4f}")
            
            timeline = ctx_data.get("timeline", {})
            print(f"\n  Timeline Points: {', '.join(sorted(timeline.keys()))}")
            
            logs = ctx_data.get("logs", [])
            print(f"\n  Log Lines: {len(logs)}")
            if logs:
                print(f"    First: {logs[0][:80]}...")
                print(f"    Last: {logs[-1][:80]}...")
            
        except Exception as exc:
            print(f"[FAIL] Error parsing context file: {exc}")
            return False
    
    # Check sprint-state.json
    state_file = REPO_ROOT / "sprint-state.json"
    if state_file.exists():
        print(f"\n[PASS] Found sprint-state.json")
        try:
            state_data = json.loads(state_file.read_text())
            print(f"  Correlation ID: {state_data.get('correlation_id')}")
            print(f"  Sprint: {state_data.get('sprint_id')}")
            print(f"  Stories Executed: {state_data.get('stories_done', 0)}/{state_data.get('total_stories', 0)}")
        except Exception as exc:
            print(f"[FAIL] Error parsing state file: {exc}")
            return False
    else:
        print(f"\n[WARN] sprint-state.json not found")
    
    # Check sprint-summary.md
    summary_file = REPO_ROOT / "sprint-summary.md"
    if summary_file.exists():
        print(f"\n[PASS] Found sprint-summary.md")
        summary_text = summary_file.read_text()
        print(f"  Length: {len(summary_text)} bytes")
    else:
        print(f"\n[WARN] sprint-summary.md not found")
    
    return True


def main():
    """Run all tests."""
    
    print("\n[START] Sprint Agent Test Suite for project 53-refactor\n")
    
    # Test 1: Run sprint agent with test mode
    exit_code = run_sprint_agent(sprint_id="S05", limit=3)
    
    if exit_code != 0:
        print(f"\n[FAIL] Sprint agent exited with code {exit_code}")
        return 1
    
    # Test 2: Verify telemetry
    if not verify_telemetry():
        print(f"\n[FAIL] Telemetry verification failed")
        return 1
    
    print("\n" + "=" * 70)
    print("[PASS] All tests passed!")
    print("=" * 70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
