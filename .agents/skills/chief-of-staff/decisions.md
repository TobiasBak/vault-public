# Decision log

Owned by the [chief-of-staff](SKILL.md) skill. Every call the chief of staff made or asked Tobias about, kept to calibrate when to ask. Public: no secrets or nonpublic details.

Format: `date · asked|decided · the call · why · verdict`. Tobias gives the verdict in review: right call, should have asked, or should have decided. Once it's reviewed, the lesson goes into the working section and the entry is deleted.

## Unreviewed

- 2026-10-11 · asked · Standing merge authority in Tobias's own repos · a global policy change · Tobias: yes, production stays behind staging and production branches.
- 2026-10-11 · asked · Settle the idle AX thread · it was his open thread, and the reason it was open was unknown · Tobias: yes, he had been waiting for emails.
- 2026-10-11 · decided · Compress `agents/coding-models.md` (2,915 → 1,936 words), splitting out `pi-throughput.md` · it was over the 2,000-word budget · Haiku review found nothing lost.
- 2026-10-11 · decided · Resolve the design-routing contradiction in favour of the Claude parent designing · Tobias decided that on 2026-10-07.
- 2026-10-11 · decided · Launch a dotfiles team to commit 12 orphaned files and push main, with nothing applied to hosts · the live global instructions weren't in Git.
- 2026-10-11 · decided · Retry a Pi child after one start failure and treat it as isolated · Pi was healthy in capabilities.
- 2026-10-11 · decided · Agree that rust-mutants picks up no follow-ups, and keep the budget-kill flake on watch rather than raising it · there was no consumer or measured pain.
- 2026-10-11 · decided · Settle the rust-mutants thread after the merge was verified · the work was done.
- 2026-10-11 · decided · Approve the ~$2.30, 45-min live benchmark for the context-view experiment · small cost, and only a live run answers whether v3 wins.
- 2026-10-11 · decided · Omarchy: run a read-only survey first and keep the work CoS-owned until the design exists; no team gets disk or installer access yet · the install is irreversible, and teams use the 2 TB disk · —
- 2026-10-11 · decided · Omarchy design: free-space install with the ext4 data partition shared by both OSes; Home Manager standalone on Omarchy, reusing the NixOS home modules; prove it in a VM first; launched a dotfiles team on a worktree · no data has to move, one source of truth for config, and the VM proof is reversible · —
- 2026-10-11 · asked · Omarchy partition size, deleting 132G of cleanup leftovers, LUKS, and the downtime window · irreversible or his preference · 400G Omarchy and the rest shared; wipe the whole disk; must boot unattended to T3; downtime fine
- 2026-10-11 · decided · Move the hand-made T3 slice drop-in into Nix rather than delete it · it carries live limits the repo must own, and the Omarchy work reuses the module · —
- 2026-10-11 · decided · Recreate the data filesystem with the old UUID; TPM2 auto-unlock, falling back to no LUKS; NixOS stays the boot default until cut-over; census unpushed work before the wipe despite "nothing important" · no rebuild needed, it meets his unattended-boot requirement, and the teams' worktrees live there · —
- 2026-10-11 · decided · Omarchy: shrink instead of wipe, delete the disposable bulk first, no NAS backup, drop the --wipe mode · same end state as Tobias's call, but Orderready's 22 worktrees survive and nothing needs copying anywhere · —
- 2026-10-11 · decided · Omarchy gets 1T and data keeps ~0.86T, not the whole disk · Tobias offered 1T or the whole disk; the whole disk would destroy the Orderready worktrees again, and the NixOS NVMe can become bulk/games storage after cut-over · —
- 2026-10-11 · decided · The delete list keeps all of orderready/ and deletes all Poly data, including the 604G capture DB, with no re-ask; I show Tobias the list and he can veto before the window · he called the Poly campaign disposable when I named it, and the census adds no new owner · Tobias: "sounds good"; running now rather than after the VM proof
- 2026-10-11 · decided · Make workspace-view v3 the default Pi extension (via dotfiles), with a rollback check in a week; no more synthetic rounds · reversible, neutral or better on 12 live runs, and real sessions are the real test · —
- 2026-10-11 · decided · Push the 12 swe-benchmarking commits after a secrets scan, and park the half-done work in PARKED.md rather than giving it a team · standing merge authority; no workstream owns the leftovers yet · —
- 2026-10-11 · decided · Standing workspace-view team: reuse the existing thread (it has the experiment context); a weekly Monday schedule pings the CoS, which dispatches; the team may self-revert past the threshold; $10 per benchmark round without asking · Tobias asked for a standing audit team; this keeps one owner and one trigger · —
- 2026-10-11 · decided · Claude context: advertise 1M and compact at 200K, not 400K, with no A/B test · Tobias skipped the test and is token-limited; 400K raises per-turn cost, while the anxiety fix alone costs nothing · —

Reviewed and already distilled: merging stepkit-geometry PR #39 was asked; the verdict was "should have decided" (see the working section).
