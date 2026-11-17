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

### L-004 - Validate the visible recipe in partial documents; require an explicit gap instead of bypassing structure.
- signal: `ac_gap` · recurrence: 1 feature(s) · scope: `document-rendering` · harmful: 0
- features: entregaveis_oficiais
- evidence: F1 / AC17 / AC33 (document-rendering)
- last seen: 2026-11-17T19:25:02Z

### L-005 - Test method labels and meanings independently from block ordering, and keep adapted applications valid.
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `document-rendering` · harmful: 0
- features: entregaveis_oficiais
- evidence: M2 / C5 (document-rendering)
- last seen: 2026-11-17T19:25:02Z

### L-006 - Exercise both sides of each slide limit separately so a different limit cannot mask the regression.
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `document-rendering` · harmful: 0
- features: entregaveis_oficiais
- evidence: M1 / C8 (document-rendering)
- last seen: 2026-11-17T19:25:02Z

### L-007 - Review example headings against their actual findings; generic closure titles do not prove analytical tone.
- signal: `spec_precision_gap` · recurrence: 1 feature(s) · scope: `document-rendering` · harmful: 0
- features: entregaveis_oficiais
- evidence: F4 / AC38 (document-rendering)
- last seen: 2026-11-17T19:25:02Z

## Quarantined (failed when applied - ignore)

A confirmed lesson that recurred alongside failure. Kept for the maintainer to review.

_none_
