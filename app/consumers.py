"""Kafka consumers for cpoe-service.

One handler per subscribed topic. Real handlers write to this service's own
database and/or publish follow-up events; stub handlers just log + audit.
"""
from __future__ import annotations

import logging

from psycopg.types.json import Json

from healthcare_common.audit import emit_audit

log = logging.getLogger("cpoe-service.consumers")

TABLE = "cpoe"


def register(svc) -> None:
    bus = svc.bus
    db = svc.db
    clients = svc.clients

    @bus.on("lab.result.available")
    def _on_lab_result_available(envelope: dict) -> None:
        data = envelope.get("data") or {}
        try:
                    # Close the corresponding order if we can trace it.
                    oid = data.get("order_id")
                    if oid:
                        db.execute(f"UPDATE {TABLE} SET status='completed', updated_at=now() "
                                   f"WHERE id = %s", (int(oid),))
        except Exception as e:
            log.exception("cpoe-service/lab.result.available handler failed: %s", e)
        emit_audit(bus, action="consume.lab.result.available", actor="system:cpoe-service",
                   target=None, details={"envelope_id": envelope.get("id")})

    @bus.on("imaging.result.available")
    def _on_imaging_result_available(envelope: dict) -> None:
        data = envelope.get("data") or {}
        try:
                    oid = data.get("order_id")
                    if oid:
                        db.execute(f"UPDATE {TABLE} SET status='completed', updated_at=now() "
                                   f"WHERE id = %s", (int(oid),))
        except Exception as e:
            log.exception("cpoe-service/imaging.result.available handler failed: %s", e)
        emit_audit(bus, action="consume.imaging.result.available", actor="system:cpoe-service",
                   target=None, details={"envelope_id": envelope.get("id")})

