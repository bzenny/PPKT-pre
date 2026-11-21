# Contribution rules for CORE

1. Update the relevant charter/ADR and decision-register entry **before** implementing financial behavior.
2. Preserve status markers: do not mark legal authorization or ratification complete without independent evidence.
3. Add tests for financial invariants, role boundaries, failure cases and rollback before implementation.
4. Run `python -m unittest discover -s tests -v && python scripts/check_core.py`.
5. Open PR with change risk, human approver, evidence, scope and finance/privacy impact. Never upload production credentials or personal data.

This package is copyright-reserved pending an explicit owner/license decision. No open-source license is implied by repository visibility.
