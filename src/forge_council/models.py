"""Dataclass mirrors of interchange payloads (schemas in schemas/forge_council/v1/)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


@dataclass
class Milestone:
    schema_version: Literal["1"] = "1"
    milestone_id: str = ""
    project_id: str | None = None
    code: str = ""
    title: str = ""
    objective: str = ""
    status: str = "draft"
    priority: int = 0
    acceptance_criteria: list[str] = field(default_factory=list)
    rollback_notes: str = ""
    dependencies: list[str] = field(default_factory=list)


@dataclass
class TaskPacket:
    schema_version: Literal["1"] = "1"
    packet_id: str = ""
    milestone_id: str = ""
    role: str = ""
    objective: str = ""
    inputs_json: dict[str, Any] = field(default_factory=dict)
    constraints_json: dict[str, Any] = field(default_factory=dict)
    deliverables_json: dict[str, Any] = field(default_factory=dict)
    validation_json: dict[str, Any] = field(default_factory=dict)
    handoff_template: str | None = None
    next_role: str | None = None


@dataclass
class GateResult:
    schema_version: Literal["1"] = "1"
    gate_id: Literal["validation", "review", "approval"] = "validation"
    passed: bool = False
    run_id: str | None = None
    trace_id: str | None = None
    log_artifact_refs: list[str] = field(default_factory=list)
    details: str = ""


@dataclass
class LedgerEvent:
    schema_version: Literal["1"] = "1"
    event_id: str = ""
    timestamp: str = ""
    workspace_id: str = ""
    project_id: str = ""
    run_id: str | None = None
    trace_id: str | None = None
    span_id: str | None = None
    event_type: str = "state_transition"
    actor: Literal["human", "agent", "system"] = "system"
    payload_json: dict[str, Any] = field(default_factory=dict)


@dataclass
class Run:
    schema_version: Literal["1"] = "1"
    run_id: str = ""
    project_id: str = ""
    workspace_id: str | None = None
    milestone_id: str | None = None
    mode: Literal["local", "remote", "hybrid"] = "local"
    status: str = "pending"
    initiated_by: str | None = None
    started_at: str | None = None
    finished_at: str | None = None
    trace_id: str | None = None
    cost_summary_json: dict[str, Any] = field(default_factory=dict)
