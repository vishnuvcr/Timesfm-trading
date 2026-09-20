from __future__ import annotations

from dataclasses import dataclass, asdict
from hashlib import sha256
import json


@dataclass(frozen=True)
class SimulationRecord:
    run_id: str
    model_id: str
    license_state: str
    execution_mode: str
    feature_vintage: str
    decision: str
    reason: str
    simulated_price: float
    simulated_cost: float
    prior_hash: str = ""


class SimulationGuard:
    """Hard guard against paper/live broker execution in this research repo."""

    @staticmethod
    def validate(*, execution_mode: str, model_id: str, license_state: str) -> None:
        if execution_mode != "simulation":
            raise PermissionError("Phase 8 is non-executing simulation only.")
        if model_id.startswith("timesfm-3.0") and license_state != "research_only":
            raise PermissionError("Unexpected TimesFM 3.0 license state for simulation.")


class AuditLedger:
    def __init__(self) -> None:
        self._records: list[dict] = []

    @property
    def records(self) -> list[dict]:
        return list(self._records)

    def append(self, record: SimulationRecord) -> str:
        payload = asdict(record)
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        digest = sha256(canonical.encode("utf-8")).hexdigest()
        self._records.append({"record": payload, "hash": digest})
        return digest

    def verify(self) -> bool:
        prior = ""
        for entry in self._records:
            payload = dict(entry["record"])
            payload["prior_hash"] = prior
            canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
            expected = sha256(canonical.encode("utf-8")).hexdigest()
            if expected != entry["hash"]:
                return False
            prior = entry["hash"]
        return True
