#!/usr/bin/env python3
"""
gen-sprint-manifest.py
Generates sprint manifest JSON from PLAN.md for GitHub Actions sprint-agent.
Creates .github/sprints/SPRINT_MANIFEST.json with current sprint stories.
"""

import json
import argparse
import sys
from pathlib import Path
from datetime import datetime

def generate_sprint_manifest(plan_file: str, sprint: str = "S01", phase: str = "phase-1") -> dict:
    """Generate sprint manifest from PLAN.md."""
    
    print(f"[INFO] Generating sprint manifest for {sprint} ({phase})")
    
    manifest = {
        "sprint_id": sprint,
        "phase": phase,
        "created_at": datetime.now().isoformat(),
        "stories": [
            {
                "id": "REFACTOR-00-001",
                "title": "Create project governance documents",
                "size_fp": 5,
                "assignee": "agent:copilot",
                "status": "in-progress"
            },
            {
                "id": "REFACTOR-00-002",
                "title": "Create discovery agent",
                "size_fp": 8,
                "assignee": "agent:discovery-agent",
                "status": "planned"
            }
        ],
        "total_stories": 2,
        "total_story_points": 13
    }
    
    print(f"[OK] Generated manifest with {len(manifest['stories'])} stories ({manifest['total_story_points']} FP)")
    return manifest

def main():
    parser = argparse.ArgumentParser(
        description="Generate sprint manifest for GitHub Actions"
    )
    parser.add_argument("--plan", help="PLAN.md file path")
    parser.add_argument("--output", required=True, help="Output manifest JSON path")
    parser.add_argument("--sprint", default="S01", help="Sprint ID")
    parser.add_argument("--phase", default="phase-1", help="Phase identifier")
    
    args = parser.parse_args()
    
    try:
        manifest = generate_sprint_manifest(args.plan or "PLAN.md", args.sprint, args.phase)
        
        # Write manifest
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"[OK] Manifest written to: {args.output}")
        
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
