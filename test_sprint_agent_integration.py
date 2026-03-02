#!/usr/bin/env python3
"""
test_sprint_agent_integration.py -- Integration test for sprint agent

Tests:
1. Sprint context initialization (correlation ID, timeline)
2. LM tracer tracking (tokens, cost, duration)
3. Evidence generator (receipt creation)
4. Data model integration (story status updates)
5. All telemetry fields populated

Run: python test_sprint_agent_integration.py
"""

import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent / ".github" / "scripts"))

from sprint_context import SprintContext
from evidence_generator import EvidenceGenerator
from refactor_lm_tracer import RefactorLMTracer
from state_lock import acquire_lock, release_lock, get_lock_status
from phase_verifier import verify_d2_repo_audit

# Test configuration
REPO_ROOT = Path(__file__).parent
TEST_CORRELATION_ID = "REFACTOR-S99-20260302-testid99"
TEST_SPRINT_ID = "SPRINT-99"
TEST_STORY_ID = "REFACTOR-99-001"


def cleanup_test_artifacts():
    """Clean up test directories before running."""
    test_dirs = [
        REPO_ROOT / ".eva" / "sprints",
        REPO_ROOT / ".eva" / "traces",
        REPO_ROOT / ".eva" / "evidence",
        REPO_ROOT / ".eva" / "locks"
    ]
    for d in test_dirs:
        if d.exists():
            shutil.rmtree(d)
    print("[CLEANUP] Removed test directories")


def test_sprint_context():
    """Test SprintContext initialization and tracking."""
    print("\n=== TEST 1: Sprint Context ===")
    
    ctx = SprintContext(TEST_CORRELATION_ID, repo_root=str(REPO_ROOT))
    
    # Verify initialization
    assert ctx.correlation_id == TEST_CORRELATION_ID
    assert ctx.sprint_id == "S99"
    assert "created" in ctx.timeline
    
    # Test logging
    log_line = ctx.log("D1", "Test message")
    assert TEST_CORRELATION_ID in log_line
    assert "Test message" in log_line
    
    # Test LM call recording
    call = ctx.record_lm_call(
        model="gpt-4o-mini",
        tokens_in=1000,
        tokens_out=500,
        phase="D1",
        duration_ms=2500
    )
    assert call["model"] == "gpt-4o-mini"
    assert call["tokens_in"] == 1000
    assert call["tokens_out"] == 500
    
    # Test timeline marking
    ctx.mark_timeline("submitted")
    assert "submitted" in ctx.timeline
    
    # Test metrics update
    ctx.update_metrics(files_created=3, test_count=12)
    assert ctx.metrics["files_created"] == 3
    assert ctx.metrics["test_count"] == 12
    
    # Test summary
    summary = ctx.get_summary()
    assert summary["correlation_id"] == TEST_CORRELATION_ID
    assert summary["sprint_id"] == "S99"
    assert summary["lm_summary"]["total_calls"] == 1
    
    # Test save
    saved_path = ctx.save()
    assert saved_path.exists()
    print(f"[PASS] Context saved to {saved_path}")
    
    # Verify JSON content
    with open(saved_path) as f:
        saved_data = json.load(f)
    assert saved_data["correlation_id"] == TEST_CORRELATION_ID
    assert len(saved_data["logs"]) > 0
    
    print("[PASS] Sprint Context Test")


def test_lm_tracer():
    """Test RefactorLMTracer independently."""
    print("\n=== TEST 2: LM Tracer ===")
    
    tracer = RefactorLMTracer(TEST_CORRELATION_ID, repo_root=str(REPO_ROOT))
    
    # Record multiple calls
    call1 = tracer.record_call(
        model="gpt-4o-mini",
        tokens_in=2000,
        tokens_out=800,
        phase="D1",
        response_text="Phase 1 complete"
    )
    
    call2 = tracer.record_call(
        model="gpt-4o",
        tokens_in=1500,
        tokens_out=600,
        phase="P",
        response_text="Planning complete"
    )
    
    # Verify summary
    summary = tracer.get_summary()
    assert summary["total_calls"] == 2
    assert summary["total_tokens_in"] == 3500
    assert summary["total_tokens_out"] == 1400
    # gpt-4o should have cost, gpt-4o-mini should be free
    assert summary["total_cost_usd"] > 0  
    
    # Test save
    trace_path = tracer.save()
    assert trace_path.exists()
    print(f"[PASS] Trace saved to {trace_path}")
    
    # Verify JSON content
    with open(trace_path) as f:
        trace_data = json.load(f)
    assert trace_data["correlation_id"] == TEST_CORRELATION_ID
    assert len(trace_data["lm_calls"]) == 2
    assert trace_data["summary"]["total_calls"] == 2
    
    print("[PASS] LM Tracer Test")


def test_evidence_generator():
    """Test EvidenceGenerator."""
    print("\n=== TEST 3: Evidence Generator ===")
    
    gen = EvidenceGenerator(
        story_id=TEST_STORY_ID,
        phase="A",
        correlation_id=TEST_CORRELATION_ID,
        sprint_id=TEST_SPRINT_ID
    )
    
    # Add universal data
    gen.add_universal_data(
        title="Test story implementation",
        artifacts=["src/test.py", "tests/test_test.py"],
        test_result="PASS",
        lint_result="PASS",
        duration_ms=12500,
        commit_sha="abc123def456",
        tokens_used=2800,
        files_changed=2
    )
    
    # Add validation data
    gen.add_validation_data(
        test_exit_code=0,
        lint_exit_code=0,
        test_output="12 passed in 2.5s",
        lint_output="All checks passed"
    )
    
    # Add LM telemetry
    gen.add_lm_telemetry(
        model="gpt-4o-mini",
        tokens_in=1500,
        tokens_out=1300,
        cost_usd=0.0,
        call_count=2
    )
    
    # Generate evidence
    evidence = gen.generate()
    assert evidence["story_id"] == TEST_STORY_ID
    assert evidence["phase"] == "A"
    assert evidence["test_result"] == "PASS"
    assert evidence["lint_result"] == "PASS"
    assert evidence["duration_ms"] == 12500
    assert evidence["tokens_used"] == 2800
    assert evidence["lm_telemetry"]["model"] == "gpt-4o-mini"
    
    # Persist evidence
    evidence_path = gen.persist(REPO_ROOT / ".eva" / "evidence")
    assert evidence_path.exists()
    print(f"[PASS] Evidence saved to {evidence_path}")
    
    # Verify JSON content
    with open(evidence_path) as f:
        evidence_data = json.load(f)
    assert evidence_data["story_id"] == TEST_STORY_ID
    assert evidence_data["validation"]["test_exit_code"] == 0
    
    print("[PASS] Evidence Generator Test")


def test_state_lock():
    """Test state lock acquire/release."""
    print("\n=== TEST 4: State Lock ===")
    
    # Acquire lock
    acquired = acquire_lock(TEST_SPRINT_ID, "test-run-123", TEST_CORRELATION_ID, repo_root=str(REPO_ROOT))
    assert acquired == True
    print(f"[PASS] Lock acquired for {TEST_SPRINT_ID}")
    
    # Verify lock status
    status = get_lock_status(TEST_SPRINT_ID, repo_root=str(REPO_ROOT))
    assert status is not None
    assert status["sprint_id"] == TEST_SPRINT_ID
    assert status["correlation_id"] == TEST_CORRELATION_ID
    
    # Try to acquire again (should fail)
    acquired_again = acquire_lock(TEST_SPRINT_ID, "test-run-456", "different-id", repo_root=str(REPO_ROOT))
    assert acquired_again == False
    print("[PASS] Duplicate lock acquisition prevented")
    
    # Release lock
    released = release_lock(TEST_SPRINT_ID, repo_root=str(REPO_ROOT))
    assert released == True
    print(f"[PASS] Lock released for {TEST_SPRINT_ID}")
    
    # Verify lock is gone
    status_after = get_lock_status(TEST_SPRINT_ID, repo_root=str(REPO_ROOT))
    assert status_after is None
    
    print("[PASS] State Lock Test")


def test_data_model_fields():
    """Verify all required data model fields are present in context."""
    print("\n=== TEST 5: Data Model Fields ===")
    
    # Create full context with all tracking
    ctx = SprintContext(TEST_CORRELATION_ID, repo_root=str(REPO_ROOT))
    
    # Simulate full story execution
    ctx.mark_timeline("submitted")
    ctx.record_lm_call("gpt-4o-mini", 1000, 500, "D1", duration_ms=2000)
    ctx.mark_timeline("response")
    ctx.mark_timeline("applied")
    ctx.update_metrics(files_created=2, files_modified=1, test_count=12, lint_issues=0)
    ctx.mark_timeline("tested")
    ctx.mark_timeline("committed")
    
    summary = ctx.get_summary()
    
    # Verify all required fields for WBS layer
    required_wbs_fields = [
        "correlation_id",
        "sprint_id", 
        "timeline",
        "lm_summary",
        "metrics"
    ]
    
    for field in required_wbs_fields:
        assert field in summary, f"Missing field: {field}"
        print(f"[PASS] Field present: {field}")
    
    # Verify timeline has all 6 points
    required_timeline_points = ["created", "submitted", "response", "applied", "tested", "committed"]
    for point in required_timeline_points:
        assert point in summary["timeline"], f"Missing timeline point: {point}"
        print(f"[PASS] Timeline point: {point}")
    
    # Verify LM summary structure
    assert "total_calls" in summary["lm_summary"]
    assert "total_tokens_in" in summary["lm_summary"]
    assert "total_tokens_out" in summary["lm_summary"]
    assert "total_cost_usd" in summary["lm_summary"]
    print("[PASS] LM summary structure complete")
    
    # Verify metrics structure
    assert summary["metrics"]["files_created"] == 2
    assert summary["metrics"]["test_count"] == 12
    assert summary["metrics"]["lint_issues"] == 0
    print("[PASS] Metrics structure complete")
    
    print("[PASS] Data Model Fields Test")


def run_all_tests():
    """Run all integration tests."""
    print("="*60)
    print("SPRINT AGENT INTEGRATION TESTS -- 53-refactor")
    print("="*60)
    
    # Cleanup first
    cleanup_test_artifacts()
    
    try:
        test_sprint_context()
        test_lm_tracer()
        test_evidence_generator()
        test_state_lock()
        test_data_model_fields()
        
        print("\n" + "="*60)
        print("[PASS] ALL TESTS PASSED")
        print("="*60)
        print("\nGenerated artifacts:")
        print(f"  - Context:  .eva/sprints/S99-testid99-context.json")
        print(f"  - Trace:    .eva/traces/{TEST_CORRELATION_ID}-lm-calls.json")
        print(f"  - Evidence: .eva/evidence/{TEST_STORY_ID}-A-*.json")
        print(f"  - Lock:     .eva/locks/{TEST_SPRINT_ID}.lock (released)")
        print("\nVerify files:")
        
        # List generated files
        for artifact_dir in [".eva/sprints", ".eva/traces", ".eva/evidence"]:
            artifact_path = REPO_ROOT / artifact_dir
            if artifact_path.exists():
                files = list(artifact_path.glob("*"))
                for f in files:
                    print(f"  ✓ {f.relative_to(REPO_ROOT)}")
        
        return 0
    
    except AssertionError as e:
        print(f"\n[FAIL] Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n[FAIL] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
