#!/usr/bin/env python3
# EVA-STORY: REFACTOR-03-001
"""
sprint_context.py -- Unified Sprint Context for Telemetry & Metrics

Unified sprint execution context: correlation ID + LM tracing + timeline.

Timeline Points (6 total):
  - created:   Sprint context initialized
  - submitted: Story execution started
  - response:  LM response received
  - applied:   Code changes applied
  - tested:    Tests executed
  - committed: Changes committed to git

Usage:
    ctx = SprintContext("REFACTOR-S05-20260302-a1b2c3d4")
    ctx.log("D1", "Starting discovery phase")
    call = ctx.record_lm_call(model="gpt-4o-mini", tokens_in=1000, tokens_out=500, phase="D1")
    ctx.mark_timeline("response")
    ctx.save()  # Writes .eva/sprints/S05-a1b2c3d4-context.json
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Dict, Any, List

# Import RefactorLMTracer from same directory
from refactor_lm_tracer import RefactorLMTracer


class SprintContext:
    """
    Unified sprint execution context with telemetry tracking.
    
    Timeline Points:
      - created:   Sprint context initialized
      - submitted: Story execution started
      - response:  LM response received
      - applied:   Code changes applied
      - tested:    Tests executed
      - committed: Changes committed to git
    """
    
    def __init__(self, correlation_id: str, repo_root: Optional[str] = None):
        """
        Initialize SprintContext.
        
        Args:
            correlation_id: Full ID in format "REFACTOR-S{NN}-{YYYYMMDD}-{uuid[:8]}"
            repo_root: Path to project root (defaults to current directory)
        """
        self.correlation_id = correlation_id
        self.repo_root = Path(repo_root) if repo_root else Path.cwd()
        
        # Extract sprint_id from correlation_id (REFACTOR-S05-20260302-a1b2c3d4 -> S05)
        parts = correlation_id.split("-")
        if len(parts) >= 2 and parts[1].startswith("S"):
            self.sprint_id = parts[1]  # "S05"
        else:
            self.sprint_id = "S00"
        
        # Initialize tracer
        self.tracer = RefactorLMTracer(correlation_id, repo_root=str(self.repo_root))
        
        # Timeline tracking
        self.timeline: Dict[str, str] = {
            "created": self._now_iso()
        }
        
        # Log buffer
        self.logs: List[str] = []
        
        # Metrics
        self.metrics = {
            "files_created": 0,
            "files_modified": 0,
            "test_count": 0,
            "lint_issues": 0,
            "duration_ms": 0
        }
    
    def _now_iso(self) -> str:
        """Get current UTC timestamp in ISO format."""
        return datetime.now(timezone.utc).isoformat() + "Z"
    
    def log(self, phase: str, message: str) -> str:
        """
        Log a message with automatic correlation ID propagation.
        
        Format: [TRACE:{correlation_id}] [{phase}] [{timestamp}] {message}
        
        Args:
            phase: Phase identifier (D, P, D, C, A) or any tag
            message: Log message
        
        Returns:
            Formatted log line
        """
        timestamp = self._now_iso()
        log_line = f"[TRACE:{self.correlation_id}] [{phase}] [{timestamp}] {message}"
        
        self.logs.append(log_line)
        print(log_line, flush=True)  # Real-time visibility
        
        return log_line
    
    def record_lm_call(self, model: str, tokens_in: int, tokens_out: int, 
                      phase: str, duration_ms: int = 0,
                      response_text: str = "", 
                      error: Optional[str] = None) -> Dict[str, Any]:
        """
        Record an LM call with telemetry (delegates to tracer).
        
        Args:
            model: Model name (e.g., "gpt-4o", "gpt-4o-mini")
            tokens_in: Input tokens
            tokens_out: Output tokens
            phase: DPDCA phase
            duration_ms: Call duration in milliseconds
            response_text: Response content (truncated for logging)
            error: Error message if call failed
        
        Returns:
            LM call record
        """
        # Delegate to tracer
        call = self.tracer.record_call(
            model=model,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            phase=phase,
            response_text=response_text,
            error=error
        )
        
        # Log with ASCII arrow for Windows compatibility
        status = "FAIL" if error else "OK"
        cost = call._calculate_cost()
        self.log(phase, 
                f"LM call [{status}]: {model} | {tokens_in}->{tokens_out} tokens | ${cost:.6f} | {duration_ms}ms")
        
        return call.to_dict()
    
    def mark_timeline(self, point: str) -> str:
        """
        Mark a timeline point with current timestamp.
        
        Args:
            point: Timeline point name (submitted, response, applied, tested, committed)
        
        Returns:
            Timestamp string
        """
        timestamp = self._now_iso()
        self.timeline[point] = timestamp
        
        self.log("timeline", f"Marked: {point}")
        
        return timestamp
    
    def update_metrics(self, **kwargs):
        """
        Update sprint metrics.
        
        Args:
            **kwargs: Metric names and values (files_created, test_count, etc.)
        """
        for key, value in kwargs.items():
            if key in self.metrics:
                self.metrics[key] += value
            else:
                self.metrics[key] = value
    
    def get_summary(self) -> Dict[str, Any]:
        """Get current sprint context summary."""
        lm_summary = self.tracer.get_summary()
        
        return {
            "correlation_id": self.correlation_id,
            "sprint_id": self.sprint_id,
            "timeline": self.timeline,
            "lm_summary": lm_summary,
            "metrics": self.metrics,
            "log_count": len(self.logs)
        }
    
    def save(self, output_dir: Optional[Path] = None) -> Path:
        """
        Save sprint context to JSON file.
        
        Args:
            output_dir: Directory to save context (defaults to .eva/sprints/)
        
        Returns:
            Path to saved file
        """
        if output_dir is None:
            output_dir = self.repo_root / ".eva" / "sprints"
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"{self.sprint_id}-{self.correlation_id.split('-')[-1]}-context.json"
        filepath = output_dir / filename
        
        summary = self.get_summary()
        summary["logs"] = self.logs  # Include full logs
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
        
        # Also save LM trace separately to .eva/traces/
        self.tracer.save()
        
        self.log("save", f"Context saved to {filepath}")
        
        return filepath
