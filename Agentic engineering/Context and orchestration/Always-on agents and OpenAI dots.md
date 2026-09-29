# Always-on agents and OpenAI dots

An always-on agent keeps responsibility across conversations. It tracks unfinished work, decides when to follow up, reacts to supported events, and brings back results or decisions. A scheduler starts work at a known time; an always-on agent can also decide when waiting should end. Always-on availability does not mean continuous inference or unrestricted action.

## OpenAI dots

OpenAI's dots are cloud-based, Astra-powered agents with their own computer and browser. They can keep working while personal devices are off, delegate background work, and stay reachable through ChatGPT, calls, Slack, or Teams. Availability checked 2026-09-29. [Meet dots](https://learn.chatgpt.com/docs/dots)

The personal Pro rollout excludes the EEA, UK, and Switzerland, so it does not currently cover Denmark. Business Premium and Enterprise are rolling out worldwide; Enterprise requires administrator enablement. Rollout eligibility does not establish account access. Dot conversations do not count toward ChatGPT usage limits, but Work and Codex tasks they start count toward those products' limits. Dots are not documented as a user-selectable Sol coordinator, so Tobias's cheaper interactive model choice does not establish cheaper dot operation. [Access](https://learn.chatgpt.com/docs/dots#access)

## Responsibilities, tasks, and memory

Give an ongoing responsibility a desired result, relevant sources, authority boundaries, and conditions for notifying the user. The dot can decide when to sleep and resume. Fixed recurring work needs a saved schedule; service-event monitoring needs an explicit assignment and support from that service. Connecting a service alone does not start monitoring. [Getting started](https://learn.chatgpt.com/docs/dots/getting-started)

The dot uses conversation context, relevant ChatGPT memory, and its own persistent notes. Notes are not a complete transcript. Separate worker tasks receive selected instructions and context, not every conversation. Persistent notes do not replace authoritative repository state or the vault's knowledge owners. [[Agent context engineering]] covers reconstructable context and handoff. [Tasks and memory](https://learn.chatgpt.com/docs/dots/tasks-and-memory)

Proactive research is distinct from assigned work. It can read permitted connected information and keep private findings, but its research tools cannot send messages, change app content, or control the browser or computer. A later action still needs the relevant authorization.

## Where work runs

Cloud tasks can continue independently of a personal device. Repository-specific cloud coding needs a configured Codex cloud environment. Local tasks require a connected computer online with the ChatGPT app open. Only one personal computer can be connected at a time, and local skills need that connection.

Messaging, app permissions, and computer access are separate connections. The cloud browser has its own sessions; it does not inherit personal browser logins. Connecting a device does not expose every existing conversation or establish control of T3 Code. [Computers and apps](https://learn.chatgpt.com/docs/dots/computers-and-apps)

## Where it fits

The useful shift is from issuing each next prompt to assigning a responsibility whose inputs change over time. These are possible uses, not deployed workflows or an authorization to start them:

| Responsibility | Useful result |
| --- | --- |
| Software feedback and verification | Investigate incoming bug reports, reproduce them in an isolated running application, and prepare fixes with evidence. Fits [[AI lead developer workflow strategy]] and [[Agentic end-to-end testing]]. |
| Research and benchmark follow-through | Follow completed runs, compare immutable results, investigate failures, and surface the next decision. [[Autoresearch]] still owns controlled trials, protected evaluation, and promotion gates. |
| Platform and dependency watch | Connect relevant releases to affected projects and prepare scoped migration advice instead of a general news digest. |
| Knowledge intake | Propose reusable findings and source-backed changes to existing subject notes. Proactive research does not authorize editing this public vault or committing it. |

Use ongoing judgment for changing inputs and uncertain follow-up. Keep settled checks in deterministic tools. [[AI-era software durability]] explains why trustworthy project state, execution, and evidence matter more than building another generic agent loop.

## Review and stopping

Review delegated work in Activity and recurring work in Scheduled. Pausing the main dot does not stop every worker or cancel schedules; these need separate controls. Stopping work does not undo completed actions. Custom rules guide action review but are not deterministic guarantees or extra app permissions. A completed run is not proof that the requested result was achieved. [Controls](https://learn.chatgpt.com/docs/dots/controls)
