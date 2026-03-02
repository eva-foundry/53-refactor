#!/usr/bin/env python3
"""
seed-from-plan.py
Seeds PLAN.md stories to data model WBS layer via HTTP API.
Parses story IDs from PLAN.md and creates/updates WBS records.
"""

import json
import argparse
import re
import sys
from pathlib import Path
from datetime import datetime

try:
    import requests
except ImportError:
    print("[ERROR] requests library not found. Install: pip install requests")
    sys.exit(1)

def parse_plan_stories(plan_file: str) -> list:
    """Extract story IDs and metadata from PLAN.md."""
    stories = []
    
    try:
        with open(plan_file, 'r') as f:
            content = f.read()
        
        # Pattern: #### [PROJECT-NN-NNN] Story Title
        pattern = r'####?\s+\[([A-Z0-9\-]+)\]\s+(.+)'
        matches = re.finditer(pattern, content)
        
        for match in matches:
            story_id = match.group(1)
            title = match.group(2).strip()
            stories.append({
                "id": story_id,
                "title": title,
                "status": "planned",
                "project": "53-refactor"
            })
        
        print(f"[OK] Parsed {len(stories)} stories from PLAN.md")
        return stories
        
    except FileNotFoundError:
        print(f"[ERROR] PLAN file not found: {plan_file}", file=sys.stderr)
        sys.exit(1)

def seed_to_data_model(stories: list, data_model_url: str, project_id: str = "53-refactor"):
    """Seed stories to data model WBS layer via HTTP API."""
    
    if not data_model_url:
        print("[WARN] No data model URL provided - skipping seed")
        return
    
    print(f"[INFO] Seeding {len(stories)} stories to {data_model_url}/model/wbs/")
    
    success_count = 0
    for story in stories:
        try:
            # Prepare WBS record
            wbs_record = {
                "id": story["id"],
                "title": story["title"],
                "project_id": project_id,
                "status": story["status"],
                "size_fp": 5,  # Placeholder
                "phase": "Phase-0",
                "is_active": True
            }
            
            # PUT to data model
            url = f"{data_model_url}/model/wbs/{story['id']}"
            headers = {"X-Actor": "agent:copilot", "Content-Type": "application/json"}
            
            response = requests.put(url, json=wbs_record, headers=headers, timeout=10)
            
            if response.status_code in (200, 201):
                print(f"  [OK] {story['id']}")
                success_count += 1
            else:
                print(f"  [WARN] {story['id']} - HTTP {response.status_code}")
        
        except Exception as e:
            print(f"  [ERROR] {story['id']} - {e}")
    
    print(f"[OK] Seeded {success_count}/{len(stories)} stories")

def main():
    parser = argparse.ArgumentParser(
        description="Seed PLAN.md stories to data model WBS layer"
    )
    parser.add_argument("--plan", required=True, help="PLAN.md file path")
    parser.add_argument("--data-model-url", help="Data model base URL")
    parser.add_argument("--project", default="53-refactor", help="Project ID")
    parser.add_argument("--dry-run", action="store_true", help="Parse only, don't seed")
    
    args = parser.parse_args()
    
    try:
        # Parse stories from PLAN
        stories = parse_plan_stories(args.plan)
        
        if args.dry_run:
            print("[INFO] DRY RUN - Parsed stories (not seeding):")
            for story in stories:
                print(f"  {story['id']}: {story['title']}")
            return
        
        # Seed to data model
        seed_to_data_model(stories, args.data_model_url, args.project)
        
        print("[OK] Seed-from-plan complete")
        
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
