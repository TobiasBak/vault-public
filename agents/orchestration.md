# Orchestration

Prompting shapes one interaction, [context engineering](context-engineering.md) shapes what each inference sees, and orchestration controls execution across interactions. Add explicit graphs or loops only when routing, state, evaluation, or recovery needs more than a provider-native agent loop. See [subagent delegation](subagent-delegation.md).

## Loops and graphs

"Loop engineering" ([Osmani](https://addyosmani.com/blog/loop-engineering/)) and "graph engineering" ([LangChain](https://www.langchain.com/blog/3-years-of-graph-engineering-with-langgraph)) are 2026 labels for old concerns.

- **Loop:** progress over time. It needs a trigger, goal, durable state, context refresh, action, evaluator, recovery, budget, and finish or escalate rules. Repetition is worthless when the evaluator can't tell improvement from confident drift. [Autoresearch](autoresearch.md) is the strong form.
- **Graph:** execution topology. Nodes are code, model calls, tools, or agents; edges are sequence, routing, parallelism, joins, cycles, and human gates. Fixed graphs fit repeatable work with real dependencies or authority boundaries. Open-ended exploration needs a capable agent and a thin contract.

## Programmatic tool calling

PTC lets the model write code that calls tools and reduces their results before anything returns to context. Keep four layers apart:

- **Ordinary tool call:** the model requests a tool and the host executes it.
- **PTC:** model-written code calls tools and filters the results.
- **Agent host** (Codex, Pi, custom): registers tools, enforces permissions, and runs the loop.
- **MCP:** a discovery and invocation protocol. It doesn't run model code.

A JSON Schema grants no capability; the host does. Selecting a PTC-capable model does not expose the provider's PTC protocol in Codex or Pi.

- **OpenAI** ([docs](https://developers.openai.com/api/docs/guides/tools-programmatic-tool-calling)): JavaScript in a fresh V8 per program, with no Node, network, filesystem, or persistent state. Opt functions in with `allowed_callers: ["programmatic"]` and `output_schema`. Load deferred tools before running the program. Return each nested call's `function_call_output` with its `call_id` and an unchanged `caller`. With `store: false`, replay all items in order. `program_output` is not necessarily the final answer.
- **Anthropic** ([docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling)): Python in the code-execution container, with tools exposed as async functions. Return `tool_result` blocks with the container ID. Reusing the container preserves state. Don't reuse an OpenAI adapter.
- **Codex code mode** composes enabled tools through `functions.exec`, which is host behavior and not the Responses PTC protocol.
- **Pi codemode** (verified in installed Pi 1.0.0, 2026-10-03) runs model-written JavaScript in QuickJS, calls enabled tools through `tools`, and returns only explicit script output to model context. Enable it alongside direct tools with `"defaultTools": ["+codemode"]`; `codemode.mode: "only"` hides direct tools. The sandbox has no direct filesystem or network, but tool side effects are real and are not rolled back on script failure. This is host behavior, not the Responses PTC protocol. See [upstream docs](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/codemode.md).

**Claude Code** (checked 2.1.289, 2026-10-04) has no documented built-in equivalent for scripting arbitrary tools like Pi codemode. Its [dynamic workflows](https://code.claude.com/docs/en/workflows) run JavaScript that orchestrates subagents and keeps intermediates in script variables, returning one consolidated result. A fresh local `claude -p` initialization exposed both `Workflow` and `ToolSearch`; availability inside T3 must be checked separately. [Tool search](https://code.claude.com/docs/en/mcp#scale-with-mcp-tool-search) defers MCP definitions, not tool execution or results. Anthropic API PTC above is a separate capability, not a Claude Code setting. The `ultracode` setting proactively chooses workflows for substantive tasks; it is off by default and unset in Tobias's settings.

Use PTC for bounded stages with predictable control flow: independent lookups plus aggregation, derived follow-up calls, deterministic joins, ranking, or dedup, and shrinking large intermediates. Use direct calls when each result needs fresh judgment, an action writes or needs approval, citations must survive, or result shapes are unstable.

## Always-on agents (OpenAI dots)

An always-on agent holds a responsibility across conversations: it tracks unfinished work, decides when to follow up, and reacts to events. A scheduler starts work at a known time; an always-on agent can also decide when waiting should end.

[OpenAI dots](https://learn.chatgpt.com/docs/dots) (checked 2026-09-29) are cloud, Astra-powered agents with their own computer and browser.

- **Availability:** personal Pro excludes the EEA, UK, and Switzerland, so not Denmark. Business Premium and Enterprise are rolling out worldwide.
- **Model and limits:** dots aren't user-selectable to Sol. Dot conversations don't count toward ChatGPT limits; the Work and Codex tasks they start do.
- **Setup:** assigning a responsibility needs a desired result, sources, authority limits, and notification conditions. Connecting a service doesn't start monitoring; recurring work needs a saved schedule.
- **Memory:** the dot keeps persistent notes plus ChatGPT memory. These are not transcripts or authoritative state. Proactive research can read but not act.
- **Where work runs:** cloud repo work needs a Codex cloud environment. Local tasks need the one connected computer online with the app open. The cloud browser doesn't share personal logins.
- **Stopping:** pausing the main dot doesn't stop workers or schedules, and stopping doesn't undo completed actions.

Plausible uses: triaging and reproducing incoming bugs, following benchmark runs, mapping dependency releases to affected projects, proposing vault updates.
