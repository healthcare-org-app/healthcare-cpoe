"""Kafka consumers for cpoe-service.

One handler per subscribed topic. Handlers are best-effort logging plus
audit — services override this file to implement real cross-domain behavior.
"""
from __future__ import annotations

import logging

from healthcare_common.audit import emit_audit

log = logging.getLogger("cpoe-service.consumers")


def register(svc) -> None:
    bus = svc.bus

    @bus.on("lab.result.available")
    def _on_lab_result_available(envelope: dict) -> None:
        log.info("cpoe-service: received lab.result.available id=%s", envelope.get("id"))
        emit_audit(bus, action="consume.lab.result.available", actor="system:cpoe-service",
                   target=None, details={"envelope_id": envelope.get("id")})

    @bus.on("imaging.result.available")
    def _on_imaging_result_available(envelope: dict) -> None:
        log.info("cpoe-service: received imaging.result.available id=%s", envelope.get("id"))
        emit_audit(bus, action="consume.imaging.result.available", actor="system:cpoe-service",
                   target=None, details={"envelope_id": envelope.get("id")})

