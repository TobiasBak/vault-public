# Tailscale

## Taildrop on `pc`

Files shared through Tailscale to the device `pc` are received automatically by `taildrop-receiver.service` and placed in `~/Phone/Inbox`. Phone screenshots therefore land there without a manual receive step. Name collisions are kept with numbered suffixes.

A manual `tailscale file get` may report `0/0 files` because the background service has already drained the Taildrop inbox.

[[Projects#Dotfiles|Dotfiles]] owns the declarative service configuration in `nixos/home/tobias/desktop.nix` and remains authoritative if the destination changes.
