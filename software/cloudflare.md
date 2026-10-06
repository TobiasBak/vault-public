# Cloudflare

## API tokens

- Give Tobias a token as a policy document, not dashboard click paths. The token page regroups and renames permissions, but permission-group IDs stay stable. The dashboard's token summary exports any token as an API JSON body or a Terraform `cloudflare_account_token`, and either form can recreate it.
- Create tokens with `POST /accounts/<account_id>/tokens` and a JSON policy body, or with OpenTofu/Terraform. Either way the caller needs a token with Account API Tokens Write, so the first admin token is always a manual bootstrap.
- Resolve permission names to IDs with the List permission groups endpoint. Without a token, use the public dump in `Cloudflare-Mining/Cloudflare-Datamining`, file `data/account/token_permission_groups.json`.
- Account IDs are not secret. Keep them in repo config, and keep only tokens in a secret store.

## Terraform for tokens

Manage tokens in Terraform/OpenTofu only when the project already manages Cloudflare there with encrypted remote state. Otherwise keep the JSON policy in the repo and create the token once.

- Creating a token needs another token that can create tokens, so IaC moves the bootstrap up one level instead of removing it.
- `cloudflare_account_token` stores the token value in state, which makes the state file a secret.

## Access

- An Access application whose `destinations` are Workers must have no `domain`; Cloudflare rejects one with error 12130. Drift checks on such apps compare name, type, destinations and policies, never `domain`.
