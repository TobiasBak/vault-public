# Colab in Google AI plans

Paid Google AI plans include Colab compute at no extra cost, announced on [Google's Developers Blog](https://developers.googleblog.com/colab-is-now-part-of-your-google-ai-plan/) on 2026-09-22. State as of 2026-10-17:

- **Pro:** about 200 compute units a month. The help-page figure was [checked 2026-10-11](https://note.com/kiyo_ai_note/n/n51c2053a8be7?hl=en), and an [account owner](https://en.kocpc.com.tw/archives/25837) saw it on their account. Google's own post gives no number.
- **Ultra:** 1,000–2,000 units a month, depending on the plan, plus premium GPUs (H100) and background execution.
- **Pro accelerators,** from a [user screenshot](https://x.com/SadAlbert10/status/2111471755240055156) dated 2026-10-17: CPU (with optional High-RAM), T4, L4, G4, A100 80 GB, v5e-1 TPU and v6e-1 TPU. H100 is greyed out behind Ultra. The A100 runtime showed 167 GB system RAM, 236 GB disk and 368 GB local scratch.
- **Who qualifies:** free trials, student offers and Jio offers don't. The rollout varies by region. Units stack with a standalone Colab Pro or Pro+ balance, but each source has its own grant date.
- **Rates:** standalone Colab Pro is $9.99 for 100 units. Units burn per hour while a runtime is connected, even when it's idle; L4 costs about 3 units an hour. The current rate for each runtime is in Colab's Resources panel.
- **Kaggle:** a Pro account raises Kaggle's GPU quota to 45 hours a week.

recheck-after: 2027-01-24

## Runtime rules

From the [Colab FAQ](https://research.google.com/colaboratory/faq.html):

- Runtimes are disposable VMs. They are deleted when idle and have a maximum lifetime: 12 hours on the free tier, up to 24 hours of continuous execution on Pro+. Disconnecting returns the VM to its original state.
- With a positive unit balance, SSH, remote desktops and non-notebook use are allowed. Without one, they're banned. Hosting web services, mining and using multiple accounts are banned for everyone.
- Unverified: does a runtime driven only by the CLI, with no browser, survive a long-running exec on Pro?

## Colab CLI

The [Colab CLI](https://developers.googleblog.com/introducing-the-google-colab-cli/) is open source ([repo](https://github.com/googlecolab/google-colab-cli)), released 2026-06, and supports Linux and macOS only. Install it with `uv tool install google-colab-cli`.

- Commands: `colab new --gpu <type>`, `exec` (Python, a script or a notebook; reuses the live runtime), `download`, `log` (exports `.ipynb` or `.jsonl`), `repl`, `console` and `stop`.
- It ships `COLAB_SKILL.md`, a skill file that coding agents such as Claude Code and Codex can use.
