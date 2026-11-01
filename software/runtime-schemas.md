# Runtime schemas

Describe each untrusted input once, in a schema library that gives you the static type, the runtime decoder and, when something outside the process needs it, a JSON Schema document. Never write a type and a hand-rolled validator side by side; they drift. Where to decode and what inward code may then trust is [decode once, then trust types](../agents/agent-native-codebases.md#decode-once-then-trust-types); this note covers the tools.

recheck-after: 2027-02-01

## Why it exists

Static types vanish at runtime or never describe incoming bytes. `JSON.parse` returns `any`, `json.loads` returns `Any`, and a TypeScript `as Foo` is a promise the compiler believes. Data from HTTP, files, env vars, queues, databases, other processes and LLM tool calls has no type until code checks it. A schema library makes that check and the type one definition:

```ts
const ReadArgs = obj({ path: str(), offset: opt(int({ minimum: 1 })) }); // pi-schema
type ReadArgs = Static<typeof ReadArgs>;                                  // { path: string; offset?: number }
compile(ReadArgs).check(input);                                           // narrows input to ReadArgs
JSON.stringify(ReadArgs);                                                 // plain JSON Schema for a tool definition
```

## When the schema leaves the process

JSON Schema is the language-neutral description other systems read: LLM tool parameters and structured output, MCP tools, OpenAPI specs and the clients generated from them, editor completion for config files. Then the schema is a contract with a consumer, so generate it from code rather than maintain it by hand ([A3 Code first](../skills/system-specs/references/api.md#a3-code-first)). Prefer a library whose native form is JSON Schema, or one whose export round-trips what you rely on; a converted schema can silently lose refinements and transforms.

## By language (versions as of 2026-11-01)

**TypeScript** (see [TypeScript 7](typescript.md) for the surrounding defaults):

- **Zod 4** (4.6): the default for validating your own app's input. Ergonomic, widest ecosystem; `z.toJSONSchema()` exports. Zod-only features such as `.refine()` and `.transform()` don't survive export.
- **TypeBox 1.x** (1.4, npm package `typebox`): schemas *are* JSON Schema, so they go straight into tool definitions and OpenAPI. Its fast compiler generates code with `new Function`.
- **pi-schema** (`@earendil-works/pi-schema` 1.4.0 in [pi-mono](https://github.com/badlogic/pi-mono/tree/main/packages/schema)): TypeBox-style builders and any-JSON-Schema validation compiled into closures, no `eval`. Its README benchmarks it close to TypeBox where `eval` works and about 100× faster where a Content Security Policy forbids it (TypeBox 42 µs vs 407 ns on a nested tagged union). Not on the npm registry as of 2026-11-01.
- **Valibot** (1.5) for smallest bundles, **ArkType** (2.2) for TypeScript-syntax definitions. Zod, Valibot and ArkType implement [Standard Schema](https://standardschema.dev), so tRPC and form libraries accept any of them without adapters.
- **AJV** (8.20): validator only; you write the JSON Schema and the type yourself. Code generation again.

Choose for the runtime: browser extensions, strict-CSP pages and Cloudflare Workers forbid string code generation, which takes AJV and TypeBox's compiler off their fast path.

**Python:**

- **Pydantic v2** (2.14): the default. `BaseModel` for records, `TypeAdapter` for bare types such as `list[Order]`, `model_validate_json` to parse and validate in one pass, `model_json_schema()` to export. OpenAI and Anthropic SDKs accept models directly.
- **msgspec** (0.22) when decode speed matters more than ecosystem; it also emits JSON Schema.
- `TypedDict` and plain `dataclass` check nothing at runtime.

**Rust:**

- **serde** derives the decoder from the type, so the type is the schema. Push value rules into constructors: newtypes with `TryFrom` and `#[serde(try_from = "String")]` make an invalid email unrepresentable instead of checked later. `garde` or `validator` add attribute rules when newtypes would be noise.
- **schemars 1.x** (1.2) derives `JsonSchema` from the same types and honors serde attributes, so tool definitions and OpenAPI come from the decoding types.
- Unknown-field policy differs by direction: persisted records tolerate unknown fields and commands reject them ([D1](../skills/system-specs/references/data.md#d1-tolerant-reads), [D8](../skills/system-specs/references/data.md#d8-strict-commands)).

## LLM providers accept a subset

Strict tool use and structured output compile the schema into a decoding grammar, so they reject or strip parts of JSON Schema. Checked 2026-11-01:

- **OpenAI** ([structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs)): every property listed in `required`, optional fields emulated as a union with `null`, `additionalProperties: false` on every object, no `allOf`, `not`, `if`/`then`/`else` or `dependent*`. At most 10 nesting levels, 5,000 properties and 1,000 enum values.
- **Anthropic** ([structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)): `additionalProperties: false` on every object, no recursion, no numeric or string-length constraints, `minItems` only 0 or 1, no external `$ref`. At most 20 strict tools, 24 optional parameters and 16 union-typed parameters per request.

The SDK helpers (`zodOutputFormat`, `zodTextFormat`, Pydantic models passed to `parse()`) send a simplified schema and validate the reply against your full one. Anthropic's raw `jsonSchemaOutputFormat` does not validate. So strict mode guarantees shape, not your constraints: still decode the model's output with your own compiled schema, and design tool schemas to the provider subset rather than discovering it as a 400.
