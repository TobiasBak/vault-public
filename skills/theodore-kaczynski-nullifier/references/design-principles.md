# Design principles

These govern repository design and changes to Theodore. Operational contracts belong in the linked references. Revise the owning principle when a durable correction changes it; do not append session history.

- **A fresh agent is the user:** an agent with no session history should be able to find the relevant behavior, change it safely, and verify the result without a human explaining the repository or repairing its work.
- **Trust is built into the codebase:** make the correct path obvious and known mistakes impossible or mechanically rejected through [structure, types, boundaries, and checks](../../../agents/agent-native-codebases.md#make-the-easiest-change-the-correct-one), rather than relying on agent memory, obedience, or model strength.
- **The codebase is the living documentation:** names, types, interfaces, ownership, executable checks, and behavioral cases should explain the system and how to change it.
- **Prose must earn its place:** keep only necessary intent, external contracts, hazards, or navigation that the executable system cannot adequately express, with [one authoritative home](agent-context.md#owners) rather than a parallel description of the code.
- **Trust evidence, not completion claims:** [independently specified behavior](black-box-tests.md#expected-output) and real execution establish what works only for the [inputs, environment, and scope actually checked](manifest.md#3-cache-verdicts), while missing or blocked verification is never success.
- **Optimize the resulting codebase, not the patch:** leave the simplest coherent system that meets the requirements, repairing ownership and removing bad examples instead of accumulating workarounds for the next agent to copy.
- **Fast feedback makes autonomy practical:** shorten the complete product [edit-to-main loop](../SKILL.md#the-loop), including navigation, verification, and coordination, without weakening the guarantees that make its output trustworthy.
- **Guarantees outlive mechanisms:** preserve behavior, safety, and necessary intent across context loss, integration, and tool replacement instead of tying them to one workflow or asking agents to remember what tools discard.
- **Fix each recurring problem at its owner:** repositories [integrate shared infrastructure](../SKILL.md#ownership) instead of rebuilding it, and Theodore should shrink as tools absorb its procedures.
- **Machinery must earn adoption:** add a capability to remove a measured cost or repair a broken contract, never merely because this skill describes it.
