"""OpenTelemetry helpers (optional dependency)."""

from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Any, Iterator

try:
    from opentelemetry import trace
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

    _HAS_OTEL = True
except ImportError:
    trace = None  # type: ignore[assignment]
    _HAS_OTEL = False


def otel_enabled() -> bool:
    return _HAS_OTEL and os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "") != ""


def configure_tracer(service_name: str = "forge-council") -> Any:
    """Configure a minimal tracer provider when OTEL SDK is installed."""
    if not _HAS_OTEL:
        return None
    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)
    if os.environ.get("FC_OTEL_CONSOLE", "").lower() in ("1", "true", "yes"):
        provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)
    return trace.get_tracer(service_name)


@contextmanager
def start_run_span(
    tracer: Any,
    name: str,
    *,
    run_id: str | None = None,
    project_id: str | None = None,
) -> Iterator[Any]:
    """Yield a span; no-op if tracer is None."""
    if tracer is None:
        yield None
        return
    attributes: dict[str, str] = {}
    if run_id:
        attributes["forge_council.run_id"] = run_id
    if project_id:
        attributes["forge_council.project_id"] = project_id
    with tracer.start_as_current_span(name, attributes=attributes) as span:
        yield span
