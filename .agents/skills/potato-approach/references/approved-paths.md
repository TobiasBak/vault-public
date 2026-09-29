# Approved implementation paths

A forbidden shortcut needs a usable alternative. A lint rule can reject an import, but it cannot supply the missing API an agent needs to finish the feature.

Design the normal change so a new agent can find where it belongs, use the supported interface, and verify the result. Prefer existing modules and libraries over a new framework when they can provide that path.

## Start with a recurring change

Choose a real task that repeatedly attracts patches or human correction. Inspect how it works end to end and identify the owner of its state and effects. Then make these answers clear in the code:

- Where does the feature live?
- Which API performs the operation, and who owns its behavior?
- How are valid states and failures represented?
- Which dependencies are allowed?
- Which existing example should an agent copy?
- Which check demonstrates the user-visible result?

Avoid making every caller reconstruct the same sequence of validation, state changes, and effects. Put the settled behavior behind its owning API. Enforce the boundary and remove competing implementations in the affected area.

## Worked example: search in a desktop app

This is an illustrative design, not a description of an existing vault project.

Suppose agents keep adding file-index reads inside UI components. The search works, but those reads block the renderer. A rule saying "keep the UI fast" leaves every agent to rediscover the same architecture.

Provide a conventional search feature:

```text
features/search/
  contract.ts
  ui/SearchView.tsx
  host/SearchService.ts
  search.test.ts
```

The names are examples. What matters is the ownership:

| Part | Responsibility |
|---|---|
| Shared contract | Search request and result types, including expected failures |
| Host service | Index access and query execution |
| UI | Call the existing typed client and render loading, result, or failure state |
| Verification | Exercise search against known data and check the visible result |

Use the application's existing transport between UI and host. Keep host dependencies out of the renderer with an import-graph check. Make its error point to the supported search client.

Now adding a search view has a direct path: use the client, render its result, and exercise the mapped search workflow. Copying the nearby example preserves the process boundary. A small direct file read no longer looks like the easiest acceptable solution.

The import check prevents this class of mistake. Measure responsiveness separately; permitted UI code can still be slow.

## Adopt the path

Use [Codebase cleanup](codebase-cleanup.md) to migrate affected callers and remove competing examples. It also owns the local recommendation on code comments. Use [Codebase hardening](codebase-hardening.md) to enforce the boundary. Verify both the normal user behavior and rejection of the known forbidden dependency.
