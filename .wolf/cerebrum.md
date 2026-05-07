# Cerebrum

> OpenWolf's learning memory. Updated automatically as the AI learns from interactions.
> Do not edit manually unless correcting an error.
> Last updated: 2026-05-07

## User Preferences

<!-- How the user likes things done. Code style, tools, patterns, communication. -->

## Key Learnings

- **Project:** 实验案例
- **SQLAlchemy single-active constraint:** To enforce "only one active record per user" (e.g. Photo.is_active), do NOT use mapper-level events (before_insert/after_insert) — they fire per-row and don't handle multiple new objects in the same flush correctly. Instead use `@db.event.listens_for(db.session, 'before_flush')` and iterate `session.new` to deactivate duplicates before the SQL flush. (See bug-001)

## Do-Not-Repeat

<!-- Mistakes made and corrected. Each entry prevents the same mistake recurring. -->
<!-- Format: [YYYY-MM-DD] Description of what went wrong and what to do instead. -->

## Decision Log

<!-- Significant technical decisions with rationale. Why X was chosen over Y. -->
