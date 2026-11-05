---
name: domain-modeling
description: Build and sharpen a project's domain language while designing. Use when terms are vague, overloaded or contested, a concept's boundaries are unclear, or names for one concept drift across code, APIs, tests and UI.
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design: challenge terms, invent edge-case scenarios, and land each term the moment it settles. This skill is for changing the model; borrowing the vocabulary the code already uses needs no skill.

The code is the glossary. A settled term lives in the names of types, modules, tables, enums, API fields, CLI commands, tests and UI copy, spelled one way everywhere. Never create a `GLOSSARY.md`, glossary map or ADR directory: a parallel glossary drifts from the code, and later sessions trust its stale claims. An existing one is evidence of intended language, not authority over the code; surface where they disagree.

Spend this rigor on concepts specific to the domain, not general programming concepts such as timeouts, retries or error types.

## During the session

### Challenge against the code's language

When the user uses a term that conflicts with the names the code already uses, call it out immediately: "The code calls this a Reservation, but you mean something that survives payment. Is that a Booking?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term: "You're saying 'account': do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it before changing either: "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?"

### Land a settled term in code

When a term settles, rename every drifted identifier, type, test name, command and piece of UI copy to it in the same change, and delete the synonyms instead of aliasing them. A published API field or persisted value is a contract: migrate its consumers rather than renaming it silently.

Define what the concept is through its type: fields and constructors that exclude the states the domain forbids. When a rejected synonym keeps returning and the repository has a lint or check surface, reject it in identifiers mechanically.

### Record decisions sparingly

A modeling decision earns a durable record only when all three hold:

1. **Hard to reverse:** changing your mind later has a meaningful cost.
2. **Surprising without context:** a future reader will wonder why it was done this way.
3. **The result of a real trade-off:** there were genuine alternatives, and one was picked for specific reasons.

If any is missing, record nothing and say which test failed. Record a qualifying decision at the repository's rationale owner; where `theodore-kaczynski-nullifier` governs the repository, follow its "Where the why goes".
