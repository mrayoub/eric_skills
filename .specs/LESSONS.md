# LESSONS - auto-maintained by scripts/lessons.py

> Machine-owned. Do NOT hand-edit. Changes are overwritten on the next `lessons.py` write.
> Canonical state lives in `.specs/lessons.json`. Edit lessons only via the script.
> promote_threshold=2 distinct features · window_days=45 · quarantine_threshold=2

## Confirmed (load these at Plan/Checks)

Corroborated across multiple features. Safe to apply as guidance.

_none_

## Candidates (under observation - do NOT load as guidance yet)

Seen once or not yet corroborated. Tracked, not trusted.

### L-001 - Assert the page-size rejection boundary directly so a relaxed tolerance fails the proof.
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `document-rendering` · harmful: 0
- features: docx_pdf_visual_parity
- evidence: C9 (document-rendering)
- last seen: 2026-10-28T21:47:18Z

### L-002 - Compare layout metrics and section placement on every page of multi-page deliverables.
- signal: `spec_precision_gap` · recurrence: 1 feature(s) · scope: `document-rendering` · harmful: 0
- features: docx_pdf_visual_parity
- evidence: C3 (document-rendering)
- last seen: 2026-10-28T21:47:18Z

### L-003 - Assert rendered document state and content occurrence counts when parity requires no duplication.
- signal: `spec_precision_gap` · recurrence: 1 feature(s) · scope: `document-rendering` · harmful: 0
- features: docx_pdf_visual_parity
- evidence: C6 (document-rendering)
- last seen: 2026-10-28T21:47:18Z

## Quarantined (failed when applied - ignore)

A confirmed lesson that recurred alongside failure. Kept for the maintainer to review.

_none_
