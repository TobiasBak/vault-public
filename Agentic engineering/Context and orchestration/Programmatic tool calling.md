# Programmatic tool calling

Programmatic tool calling, or PTC, lets a model write code that invokes tools and processes their results before returning selected output to model context. OpenAI and Anthropic provide different managed implementations. It is not a synonym for ordinary function calling or for controlling an agent from application code.

Provider runtime distinctions checked 2026-09-26. Codex and Pi are separate agent hosts with their own tool registries, permissions, and execution loops. Selecting a PTC-capable model does not expose a provider's public PTC protocol automatically.

## Capability boundary

Keep four layers distinct:

- **Ordinary tool calling:** the model requests a named tool with arguments; the host validates and executes it.
- **PTC:** model-written code calls eligible tools, coordinates their execution, and reduces intermediate results before returning them to model context.
- **Agent host:** Codex, Pi, or a custom application registers concrete capabilities, enforces permissions, executes client-owned calls, and continues the model loop.
- **MCP:** a protocol for tool discovery and invocation between a host and a server. It does not itself execute model-generated orchestration code.

A JSON Schema describes what the model may request. It grants no filesystem, network, process, or third-party capability. The runtime and host remain the authority for access and side effects.

## OpenAI implementation

OpenAI Responses PTC runs JavaScript with top-level `await` in a fresh V8 runtime. It does not supply Node.js, package installation, direct network access, a general filesystem, subprocesses, or persistent JavaScript state between programs. External effects use enabled tools; the application validates and executes client-owned functions.

Opt eligible functions in with `allowed_callers` containing `programmatic`; describe structured returns with `output_schema`. Load deferred tools before running a program because Tool Search remains at the top-level Responses layer.

For each nested client-owned call, return `function_call_output` with its `call_id` and unchanged `caller`. Continue stored responses with `previous_response_id`; with `store: false`, replay program, reasoning, call/output, and program-output items in order. A `program_output` is not necessarily the final response. [OpenAI PTC](https://developers.openai.com/api/docs/guides/tools-programmatic-tool-calling)

## Anthropic implementation

Anthropic PTC runs Python in its code-execution container. Eligible client tools appear as async functions. Python can combine calls, await results supplied by the application, and process them without sending each intermediate result through the model.

Use the supported code-execution tool version in `allowed_callers` and return Claude's `tool_result` blocks with the container identity needed to resume execution. Reusing a container can preserve state, unlike OpenAI's fresh JavaScript runtimes. The request items, caller fields, runtime capabilities, and retention rules are provider-specific; do not reuse an OpenAI adapter unchanged. [Anthropic PTC](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling)

## When programmatic composition helps

Use PTC for bounded stages with predictable control flow and structured outputs:

- independent lookups followed by aggregation;
- dependent calls where code can derive later arguments;
- deterministic joins, ranking, filtering, validation, or deduplication;
- large intermediates that can be reduced before reaching model context.

Prefer direct calls when one call is enough, each result needs fresh semantic judgment, an action writes data or requires approval, native citations must survive, or return shapes are not stable. Define a clear handoff between programmatic and direct stages, including allowed tools, output shape, evidence, retries, stop conditions, and side-effect limits. Compare correctness and evidence before token or latency savings. This follows [[Prompting tool-using agents]].

## Agent-host integration

Codex code mode can expose native JavaScript composition through `functions.exec`. This lets the agent compose enabled tool calls and reduce intermediate output without a custom worker or orchestration service. Use the actual session's tool definitions for runtime capabilities; host-provided helpers are not promises about the public Responses PTC protocol.

For Pi or another host, inspect the installed adapter before claiming support for a provider's program items, caller linkage, or continuation protocol. A tool extension or outbound request rewrite alone does not implement those contracts.

A deterministic orchestration tool may supply the required composition without exposing a provider protocol. Describe what the host actually does. Use the public API directly when its exact contract is needed, not merely because the task needs several tools coordinated in code.
