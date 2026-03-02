#!/usr/bin/env python3
"""
Populate missing fields in project 53 WBS records for ADO velocity tracking.

Fixes:
  - sprint: Assign to S05-S22 based on epic
  - assignee: Marco Presta as default (can be changed during execution)
  - project_id: Set to "53-refactor"
  - ado_id: Will be set after ADO sync via 38-ado-poc
"""

import requests
import json
import time
from pathlib import Path

BASE_URL = "https://marco-eva-data-model.livelyflower-7990bc7b.canadacentral.azurecontainerapps.io"
PROJECT_ID = "53-refactor"
ASSIGNEE_DEFAULT = "marco.presta@hrsdc-rhdcc.gc.ca"

# Sprint mapping: Epic -> Sprint assignment
# 115 stories across 18 sprints (S05-S22)
EPIC_SPRINT_MAP = {
    "EPIC-13": "S05",  # Frontend Admin Face (10 stories)
    "EPIC-14": "S06",  # Frontend Chat Face (10 stories)
    "EPIC-15": "S07",  # Frontend Portal Face (5 stories)
    "EPIC-11": "S08",  # Backend API Routers (10 stories)
    "EPIC-12": "S09",  # Backend Auth & Middleware (10 stories)
    "EPIC-03": "S10",  # Auth & Security (10 stories)
    "EPIC-16": "S11",  # Data Layer & Cosmos (10 stories)
    "EPIC-17": "S12",  # Observability & Logging (10 stories)
    "EPIC-18": "S13",  # Security Hardening (8 stories)
    "EPIC-19": "S14",  # Testing & QA (8 stories)
    "EPIC-20": "S15",  # Documentation (8 stories)
    "EPIC-22": "S16",  # DevOps & Deployment (6 stories)
}

def get_sprint_for_story(story_id: str) -> str:
    """Map story ID to sprint based on epic number."""
    # Extract epic number: REFACTOR-03-001 -> 03
    parts = story_id.split("-")
    if len(parts) >= 2:
        epic_num = parts[1]
        epic_key = f"EPIC-{epic_num}"
        return EPIC_SPRINT_MAP.get(epic_key, "S05")  # Default to S05
    return "S05"

def update_story(story_id: str, story_data: dict) -> bool:
    """Update a single story with missing fields."""
    try:
        # Get current record
        resp = requests.get(f"{BASE_URL}/model/wbs/{story_id}", timeout=10)
        if resp.status_code != 200:
            print(f"  ❌ [{story_id}] Not found (404)")
            return False
        
        current = resp.json()
        row_version = current.get("row_version")
        
        # Prepare update
        update_data = {
            "sprint": story_data.get("sprint"),
            "assignee": story_data.get("assignee"),
            "project_id": story_data.get("project_id"),
        }
        
        # Keep existing fields (rule: strip audit columns, keep domain fields)
        for key in current.keys():
            if key not in ["layer", "modified_by", "modified_at", "created_by", "created_at", "row_version", "source_file", "obj_id"]:
                if key not in update_data:
                    update_data[key] = current[key]
        
        # PUT update
        put_resp = requests.put(
            f"{BASE_URL}/model/wbs/{story_id}",
            json=update_data,
            headers={"X-Actor": "agent:copilot", "Content-Type": "application/json"},
            timeout=10
        )
        
        if put_resp.status_code in [200, 201]:
            new_version = put_resp.json().get("row_version")
            print(f"  ✅ [{story_id}] Updated (sprint={update_data['sprint']}, assignee set)")
            return True
        else:
            print(f"  ❌ [{story_id}] PUT failed: {put_resp.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ [{story_id}] Error: {str(e)}")
        return False

def main():
    print("=" * 70)
    print("PROJECT 53: POPULATE MISSING ADO VELOCITY FIELDS")
    print("=" * 70)
    print()
    
    # Read seeded stories from .eva/greenfield-stories.json
    manifest_path = Path("C:\\AICOE\\eva-foundry\\53-refactor\\.eva\\greenfield-stories.json")
    
    if not manifest_path.exists():
        print(f"❌ Manifest not found: {manifest_path}")
        print("   Run Phase 2 story generation first")
        return
    
    with open(manifest_path) as f:
        manifest = json.load(f)
    
    # Extract stories from epics structure
    stories = []
    epics = manifest.get("epics", [])
    for epic in epics:
        epic_stories = epic.get("stories", [])
        stories.extend(epic_stories)
    
    print(f"Found {len(stories)} stories across {len(epics)} epics")
    print()
    
    # Update each story
    success_count = 0
    failure_count = 0
    
    print("Updating stories with sprint, assignee, and project_id...")
    print("-" * 70)
    
    for idx, story in enumerate(stories, 1):
        story_id = story.get("id")
        if not story_id:
            continue
        
        # Determine sprint
        sprint = get_sprint_for_story(story_id)
        
        # Prepare update data
        update_data = {
            "sprint": sprint,
            "assignee": ASSIGNEE_DEFAULT,
            "project_id": PROJECT_ID,
        }
        
        # Update
        if update_story(story_id, update_data):
            success_count += 1
        else:
            failure_count += 1
        
        # Rate limit (be nice to the API)
        if idx % 10 == 0:
            time.sleep(0.5)
    
    print("-" * 70)
    print()
    print(f"RESULTS:")
    print(f"  ✅ Updated: {success_count}")
    print(f"  ❌ Failed: {failure_count}")
    if (success_count + failure_count) > 0:
        print(f"  📊 Success Rate: {100 * success_count / (success_count + failure_count):.1f}%")
    print()
    
    if success_count > 0:
        print("NEXT STEPS:")
        print("  1. Verify updates in data model:")
        print("     Invoke-RestMethod 'https://marco-eva-data-model.../model/wbs/REFACTOR-03-001'")
        print()
        print("  2. Create ADO work items via 38-ado-poc ADO sync (Pull mode)")
        print()
        print("  3. Populate ado_id field after work items created")
        print()
        print("  4. Ready for Phase 3 execution (S05-S22)")

if __name__ == "__main__":
    main()
