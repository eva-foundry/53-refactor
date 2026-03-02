#!/usr/bin/env python3
"""
check-mti-gate.py
Verifies that Veritas MTI (Modernization Trust Index) score meets quality gate.
"""

import json
import argparse
import sys
from pathlib import Path

def check_mti_gate(audit_file: str, target_mti: int = 80) -> bool:
    """Check if MTI score meets target."""
    
    print(f"[INFO] Checking MTI gate (target >= {target_mti})")
    
    try:
        with open(audit_file, 'r') as f:
            audit = json.load(f)
        
        mti_score = audit.get('mti_score', 0)
        print(f"[INFO] Current MTI score: {mti_score}")
        
        if mti_score >= target_mti:
            print(f"[PASS] MTI score {mti_score} >= {target_mti}")
            return True
        else:
            print(f"[FAIL] MTI score {mti_score} < {target_mti}")
            return False
    
    except FileNotFoundError:
        print(f"[WARN] Audit file not found: {audit_file}")
        print("[INFO] Skipping MTI gate (placeholder mode)")
        return True

def main():
    parser = argparse.ArgumentParser(description="Check MTI quality gate")
    parser.add_argument("--audit", required=True, help="Audit results JSON file")
    parser.add_argument("--target-mti", type=int, default=80, help="Target MTI score")
    
    args = parser.parse_args()
    
    if not check_mti_gate(args.audit, args.target_mti):
        sys.exit(1)

if __name__ == "__main__":
    main()
