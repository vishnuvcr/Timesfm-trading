import pytest

from src.simulation.audit import AuditLedger, SimulationGuard, SimulationRecord


def test_phase8_guard_rejects_non_simulation() -> None:
    with pytest.raises(PermissionError):
        SimulationGuard.validate(
            execution_mode="paper",
            model_id="timesfm-3.0-pytorch",
            license_state="research_only",
        )


def test_phase8_guard_accepts_nonexecuting_3() -> None:
    SimulationGuard.validate(
        execution_mode="simulation",
        model_id="timesfm-3.0-pytorch",
        license_state="research_only",
    )


def test_audit_ledger_hash_chain_verifies() -> None:
    ledger = AuditLedger()
    h1 = ledger.append(
        SimulationRecord(
            run_id="r1",
            model_id="timesfm-3.0-pytorch",
            license_state="research_only",
            execution_mode="simulation",
            feature_vintage="v1",
            decision="hold",
            reason="cost gate",
            simulated_price=100.0,
            simulated_cost=1.0,
        )
    )
    ledger.append(
        SimulationRecord(
            run_id="r1",
            model_id="timesfm-3.0-pytorch",
            license_state="research_only",
            execution_mode="simulation",
            feature_vintage="v1",
            decision="buy",
            reason="edge gate",
            simulated_price=101.0,
            simulated_cost=1.0,
            prior_hash=h1,
        )
    )
    assert ledger.verify()


def test_audit_ledger_detects_tampering() -> None:
    ledger = AuditLedger()
    ledger.append(
        SimulationRecord(
            run_id="r1",
            model_id="timesfm-3.0-pytorch",
            license_state="research_only",
            execution_mode="simulation",
            feature_vintage="v1",
            decision="hold",
            reason="stale data",
            simulated_price=100.0,
            simulated_cost=0.0,
        )
    )
    ledger._records[0]["record"]["decision"] = "buy"
    assert not ledger.verify()
