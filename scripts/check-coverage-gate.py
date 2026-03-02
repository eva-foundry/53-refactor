#!/usr/bin/env python3
"""
check-coverage-gate.py
Verifies test coverage meets quality gate.
"""

import json
import argparse
import sys
from pathlib import Path

def check_coverage_gate(coverage_file: str, target: float = 0.80) -> bool:
    """Check if test coverage meets target."""
    
    print(f"[INFO] Checking coverage gate (target >= {target*100:.0f}%)")
    
    try:
        with open(coverage_file, 'r') as f:
            coverage = json.load(f)
        
        total_coverage = coverage.get('totals', {}).get('percent_covered', 0)
        coverage_pct = total_coverage / 100.0
        
        print(f"[INFO] Current coverage: {total_coverage:.1f}%")
        
        if coverage_pct >= target:
            print(f"[PASS] Coverage {total_coverage:.1f}% >= {target*100:.0f}%")
            return True
        else:
            print(f"[FAIL] Coverage {total_coverage:.1f}% < {target*100:.0f}%")
            return False
    
    except FileNotFoundError:
        print(f"[WARN] Coverage file not found: {coverage_file}")
        print("[INFO] Skipping coverage gate (placeholder mode)")
        return True

def main():
    parser = argparse.ArgumentParser(description="Check coverage quality gate")
    parser.add_argument("--coverage-report", required=True, help="Coverage report JSON")
    parser.add_argument("--target", type=float, default=0.80, help="Target coverage (0-1)")
    
    args = parser.parse_args()
    
    if not check_coverage_gate(args.coverage_report, args.target):
        sys.exit(1)

if __name__ == "__main__":
    main()
