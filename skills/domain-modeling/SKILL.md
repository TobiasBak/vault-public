---
name: domain-modeling
description: Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a GLOSSARY.md, recording or editing an ADR, when terms are vague, overloaded or contested, when names for one concept drift across code, APIs, tests and UI, or when an ADR or other recorded decision conflicts with the task.
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design: challenge terms, invent edge-case scenarios, and write each term down the moment it settles. This skill is for changing the model; reading `GLOSSARY.md` to borrow its vocabulary needs no skill.

The glossary and the code speak one language. A settled term goes into `GLOSSARY.md` and into the names of types, modules, tables, enums, API fields, CLI commands, tests and UI copy, spelled one way everywhere.

## File structure

Terms live in one root `GLOSSARY.md`, or in per-context glossaries that a root `GLOSSARY-MAP.md` lists. [GLOSSARY-FORMAT.md](GLOSSARY-FORMAT.md) owns both formats, how to tell which applies, and lazy creation.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `GLOSSARY.md` or the code, call it out immediately: "Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term: "You're saying 'account': do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it before changing either: "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?"

### Update GLOSSARY.md inline

When a term is resolved, update `GLOSSARY.md` right there. Don't batch these up: capture them as they happen.

`GLOSSARY.md` holds terms and nothing else: no implementation details, decisions, specs or scratch notes. It shrinks as often as it grows. When an entry has absorbed implementation detail, cut it back to what the thing is.

### Land the term in code

In the same change, rename every drifted identifier, type, test name, command and piece of UI copy to the settled term, and delete the synonyms instead of aliasing them. A published API field or persisted value is a contract: migrate its consumers rather than renaming it silently.

Define what the concept is through its type: fields and constructors that exclude the states the domain forbids. When a term under `_Avoid_` keeps returning and the repository has a lint or check surface, reject it in identifiers mechanically.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse:** changing your mind later has a meaningful cost.
2. **Surprising without context:** a future reader will wonder why it was done this way.
3. **The result of a real trade-off:** there were genuine alternatives, and one was picked for specific reasons.

If any is missing, skip the ADR and say which test failed. Use the format in [ADR-FORMAT.md](ADR-FORMAT.md).

### Treat ADRs as dated evidence

An ADR records past reasoning, often agent-written and accepted without much scrutiny. It is not a rule. The user's current instruction outranks it: name the conflicting ADR, do what was asked, and rewrite or delete the ADR in the same change. When the code or requirements have moved past an ADR, challenge it with what changed instead of obeying it. Never refuse or stall by citing one. Glossary entries age the same way.
