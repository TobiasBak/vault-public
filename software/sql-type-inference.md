# SQL-file type inference

Type-safe queries need not require an ORM query language. SQL-file inference keeps SQL as the query source while deriving the TypeScript input and result contracts. Consider SQL-first access when an ORM's main value would be query typing.

## colinhacks demo

[Post and video, 2026-10-22](https://x.com/colinhacks/status/2113145042454134986): "type inference from .sql files has been achieved internally" and "ORMs are toast."

The video shows a `.sql` file imported directly into TypeScript and executed with the `postgres` client:

```sql
-- get_users.sql
select id, name, role from users
where email = :email;
```

```ts
import postgres from "postgres";
import getUsers from "./get_users.sql";

const db = postgres(process.env.DATABASE_URL!);
const result = await getUsers.run(db, { email: "user@example.com" });
```

Observed in the editor:

- Selecting `id, name, role` produces rows with `id: number`, `name: string`, and `role: "admin" | "member"`, without handwritten result types.
- Adding `where email = :email` requires a second argument containing `email: string`. Omitting it produces a TypeScript error.
- The filtered result becomes a single row or `null`, rather than an array. The schema and basis for this cardinality inference are not shown.

## What to take from it

The useful claim is that ordinary SQL can offer typed parameters, precise result shapes, and editor feedback. "ORMs are toast" is the author's conclusion, not something the clip establishes. Migrations, transactions, relation loading, and dynamic query composition still need owners.

The post describes internal work and names no package or release. It does not establish schema discovery, code-generation or plugin requirements, CLI/CI type-checking, supported SQL coverage, or runtime correctness. Treat it as a capability demo, not an adoption recommendation. In particular, verify [TypeScript 7 tooling compatibility](typescript.md#adoption-boundaries) before choosing an implementation.
