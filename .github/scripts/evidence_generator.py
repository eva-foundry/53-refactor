#!/usr/bin/env python3
"""
evidence_generator.py -- Generate Evidence Receipts for Story Completion

Creates immutable evidence records with:
- Story metadata (id, title, phase, sprint)
- Validation results (test, lint)
- Telemetry (tokens, cost, duration)
- Artifacts (files created/modified, commits)
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, List


class EvidenceGenerator:
    """Generates evidence receipts for stories in the DPDCA cycle."""
    
    def __init__(self, story_id: str, phase: str = "A", 
                 correlation_id: Optional[str] = None,
                 sprint_id: Optional[str] = None):
        """
        Initialize evidence generator.
        
        Args:
            story_id: Story ID (e.g., "REFACTOR-03-001")
            phase: DPDCA phase ("D", "P", "D", "C", "A")
           correlation_id: From SprintContext
            sprint_id: Sprint identifier (e.g., "S05")
        """
        self.story_id = story_id
        self.phase = phase
        self.correlation_id = correlation_id
        self.sprint_id = sprint_id
        self.timestamp = datetime.now(timezone.utc).isoformat() + "Z"
        
        # Universal fields (present in all evidence types)
        self.universal = {
            "test_result": "UNKNOWN",
            "lint_result": "UNKNOWN",
            "duration_ms": 0,
            "artifacts": [],
            "tokens_used": 0,
            "files_changed": 0
        }
        
        # Type-specific fields
        self.type_fields = {}
    
    def add_universal_data(self, 
                          title: Optional[str] = None,
                          artifacts: Optional[List[str]] = None,
                          test_result: str = "PASS",
                          lint_result: str = "PASS",
                          duration_ms: int = 0,
                          commit_sha: Optional[str] = None,
                          tokens_used: int = 0,
                          test_count_before: int = 0,
                          test_count_after: int = 0,
                          files_changed: int = 0):
        """Add universal fields present in all evidence types."""
        if title:
            self.universal["title"] = title
        if artifacts:
            self.universal["artifacts"] = artifacts
        self.universal["test_result"] = test_result
        self.universal["lint_result"] = lint_result
        self.universal["duration_ms"] = duration_ms
        if commit_sha:
            self.universal["commit_sha"] = commit_sha
        self.universal["tokens_used"] = tokens_used
        self.universal["test_count_before"] = test_count_before
        self.universal["test_count_after"] = test_count_after
        self.universal["files_changed"] = files_changed
    
    def add_validation_data(self, test_exit_code: int, lint_exit_code: int,
                           test_output: str = "", lint_output: str = ""):
        """Add validation gate results."""
        self.type_fields["validation"] = {
            "test_exit_code": test_exit_code,
            "lint_exit_code": lint_exit_code,
            "test_output_preview": test_output[:500] if test_output else "",
            "lint_output_preview": lint_output[:500] if lint_output else ""
        }
    
    def add_lm_telemetry(self, model: str, tokens_in: int, tokens_out: int, 
                        cost_usd: float, call_count: int = 1):
        """Add LM call telemetry."""
        self.type_fields["lm_telemetry"] = {
            "model": model,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "cost_usd": round(cost_usd, 6),
            "call_count": call_count
        }
    
    def generate(self) -> Dict[str, Any]:
        """
        Generate the evidence receipt.
        
        Returns:
            Complete evidence dictionary
        """
        evidence = {
            "story_id": self.story_id,
            "phase": self.phase,
            "timestamp": self.timestamp,
            "correlation_id": self.correlation_id,
            "sprint_id": self.sprint_id,
        }
        
        # Merge universal and type-specific fields
        evidence.update(self.universal)
        evidence.update(self.type_fields)
        
        return evidence
    
    def persist(self, output_dir: Path) -> Path:
        """
        Write evidence to disk.
        
        Args:
            output_dir: Directory to write evidence (e.g., .eva/evidence/)
        
        Returns:
            Path to written file
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Filename: STORY-ID-PHASE-TIMESTAMP.json
        timestamp_short = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        filename = f"{self.story_id}-{self.phase}-{timestamp_short}.json"
        filepath = output_dir / filename
        
        evidence = self.generate()
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(evidence, f, indent=2)
        
        print(f"[INFO] Evidence written: {filepath}")
        
        return filepath
    
    @staticmethod
    def load(filepath: Path) -> Dict[str, Any]:
        """Load evidence from disk."""
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
