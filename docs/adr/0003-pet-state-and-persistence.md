# ADR 0003: Deterministic Pet State Engine with SQLite WAL Persistence

## Status

Accepted

## Context

The original voice assistant extracts a business lead profile from transcripts and stores call data in SQLite WAL mode. GLITCH needs a similar structured layer, but for pet vitals and emotional continuity.

## Decision

Replace lead-intake extraction with a deterministic Pet State Engine backed by SQLite WAL.

The LLM may classify sentiment or propose a tone, but durable state changes must go through testable rules. SQLite stores current pet state, interaction timeline, and share/rescue metadata.

## Consequences

- Moods remain explainable and testable.
- GLITCH can remember neglect and affection across browser sessions.
- Time-decay behaviours can run at session startup without background infrastructure.
- The project avoids a heavyweight database until real user/account needs exist.
