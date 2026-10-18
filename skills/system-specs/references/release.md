# Release and deploy

Scope: every change to production behavior, from merge to running on servers and clients. Builds on the [data catalog](data.md): additive changes, a minimum supported version, servers before clients.

Principles:
- Git is the only path to production.
- One combined version per build.
- A production release is a human action by default. A project may opt into automatic promotion.
- Data never rolls back. Code may roll back automatically.
- Gates are enforced outside the agents that write the changes.

## Path to production

### R1 Everything goes through git

Code, schema, config, flag values, client builds and infrastructure live in git and reach production only through the release pipeline.

Reason: config and flag pushes that skip staged rollout cause major outages. Cloudflare's [2019 outage](https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/) was a WAF rule pushed globally outside the software rollout.

Enforcement: production credentials exist only in the pipeline; production config has no other write path.

### R2 One version, known running state

Every artifact built from a commit carries that commit's single version. A release manifest links artifact digests, migrations and verification results to it. A deployment inventory records what actually runs, including mixed versions mid-rollout and client adoption.

Reason: "client ≥ X" and "server has migration Y" stay simple comparisons, and "what is running" has one answer.

Enforcement: the build stamps the version; the pipeline writes the manifest and inventory; binaries report their version.

### R3 Built once, signed, verified

Each release is built once from its commit, signed, and verified before every deploy or install. The same artifact moves through every stage. Agents have no production credentials and can't waive gates. Reproducible builds and SBOMs wait until a customer or regulator asks.

Reason: prevents deploying an untested or substituted build, and an agent shipping its own unverified change.

Enforcement: deploy and install steps reject unsigned or unknown digests; credentials are scoped to the pipeline.

### R4 Continuous staging

Main deploys to staging automatically whenever its gates pass. Staging runs the same artifacts, migrations and pipeline as production, has its own client update channel with internal machines as the earliest cohort, and holds synthetic or anonymized data, never customer personal data.

Reason: staging is where Tobias playtests what's coming, and where the pipeline itself is exercised before production.

Enforcement: the pipeline deploys staging and production from the same manifest; staging has no access to production data.

### R5 Human-promoted, at most daily

Tobias promotes staging to production after playtesting. At most one ordinary release a day, typically less. A release carries server and clients together under one version. Generated release notes list the merged changes and highlight approval-class changes: a minimum-version bump, a destructive [D5](data.md#d5-two-step-destructive-changes) step, auth, payment and infrastructure.

Reason: users shouldn't get an update every day, and the release decision belongs to a human who has seen the build. One promotion a day is cheap.

Enforcement: the pipeline refuses a second ordinary promotion the same day; release notes are generated from the diff, and approval-class detection runs on it.

### R6 Hotfixes go through main

Only an incident or bug forces an extra release. The fix lands on main first, then takes a fast track: touched checks plus smoke tests, a short staging bake, and the normal staged production rollout. Never cherry-pick onto the release branch. A kill-switch flip (R14) is faster when a flag covers the problem.

Reason: a fix that skips main is erased by the next release. The fast track shortens waiting, never steps.

Enforcement: the release branch accepts only promotions of commits already on main.

## Rollout

### R7 Executable deploy order

Migrations, then server, then clients. The order is a dependency graph that advances only on success and rechecks its preconditions when each step executes.

Reason: a consumer outrunning its provider or migration breaks, and separately passing pipelines race. Enforces [D8](data.md#d8-strict-commands) and [D11](data.md#d11-migration-execution).

Enforcement: the pipeline graph; a client release is blocked until its server version is live.

### R8 Verified server rollout

Server rollouts are staged. A stage is verified by synthetic user journeys in production under a test identity (sign in, read, write, background work completes) and by the new version's error and latency rates compared with the previous version. Promotion needs a minimum amount of observed traffic; no traffic means not verified, never pass.

Reason: a health check proves the process is up, not that orders go through.

Enforcement: the rollout controller gates each stage on the journeys and per-version rates (R16).

### R9 Automatic abort

When a stage fails, the server reverts to the previous build and the client rollout halts, before anyone is paged. Data never rolls back; the real fix ships forward. A bad client build can't be pulled back from installed machines: it is fixed by a higher-numbered build, and server-side flags neutralize the bad feature meanwhile.

Reason: the data catalog keeps the previous server build compatible, so reverting code is the fastest safe mitigation. Same-version or downgraded client builds strand users.

Enforcement: the rollout controller performs the abort; the update feed only offers versions above the installed one.

### R10 Staged client rollout

New client builds go to stable cohorts (the same machines first every time): 1%, 10%, 50%, 100%. Each step needs a minimum number of reporting installs and halts automatically when that version's crash or error rate rises against the previous version. Customers may opt into the early cohort.

Reason: limits a bad client build to a few machines.

Enforcement: the update server assigns cohorts and gates steps on per-version rates (R16).

### R11 Client self-update

Clients download in the background, verify the signature, and activate on the next restart; a client below the minimum supported version restarts and activates immediately, keeping unsent work ([D13](data.md#d13-minimum-supported-version)). The working install stays until the new one is verified. A failed delta update falls back to the full package. A signed repair path works even when the app won't start.

Reason: without the repair path, a build that crashes on startup can never receive its fix.

Enforcement: black-box cases: interrupted update leaves a working install; a corrupt package is rejected; repair recovers a client that fails to start.

### R12 Raising the minimum version

Raising the minimum is approval-class. It requires the qualifying build in every channel (auto-update, offline installer, enterprise deployment), an "update required by …" warning to affected clients first, with their count known, and a blocked screen that says to update or contact IT. Admins may delay updates but never below the minimum; they get signed offline installers and a view of which machines are blocked and why.

Reason: silent updating still leaves a tail; Chrome had about 3% behind after 21 days ([2009 study](https://techzoom.net/whitepapers/why_silent_updates_boost_security_2009.pdf)). The warning length is set per product.

Enforcement: the pipeline refuses the minimum bump until the build is published in every channel and the warning phase has run.

### R13 Stale web clients

A web client detects it runs an outdated build, saves unsent input, and reloads into the current one. Old static assets stay available long enough for open sessions.

Reason: a tab opened yesterday runs old code against today's server.

Enforcement: black-box case: an old build's tab hits a new server, keeps its input and reloads.

## Control

### R14 Flags

Flags separate deploying code from users seeing it: gradual exposure and kill switches. Flag values live in git and the server delivers them to clients at runtime; a flip goes through a fast config path, staged and logged. Every flag has an owner and expiry. An expired flag fails the build and forces a cleanup PR; it never flips itself in production. Kill switches are a separate, permanent category with periodic review. Work that belongs together ships together; half-built work is never visible to users.

Reason: flags turn a bad feature off in seconds instead of a release plus client updates. Every flag doubles code paths, and agents copy what they read, so stale flags spread.

Enforcement: a build check on flag expiry and ownership; flag changes use the R1 pipeline.

### R15 Automatic freeze

Ordinary releases are blocked while production alarms fire or the error budget is spent. Fixes and kill-switch flips are exempt.

Reason: new changes during an incident hide its cause and lengthen it.

Enforcement: the pipeline reads alarm and error-budget state before promoting.

### R16 Version-attributed telemetry

Every log, trace, metric and crash report carries the version. Every release, config push and flag flip writes a deploy marker. Error and crash rates are compared per version as rates, not totals.

Reason: R8, R9 and R10 can't compute "the new version is worse" without it.

Enforcement: the telemetry setup injects the version (OpenTelemetry `service.version`); the pipeline writes markers.
