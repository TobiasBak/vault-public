# Cloudflare

## API tokens

- Give Tobias a token as a policy document with permission-group IDs, not dashboard click paths. The token page regroups and renames permissions; the IDs stay stable. The dashboard's token summary exports the same token as an API body or a Terraform `cloudflare_account_token`.
- Account IDs are not secret. Keep them in repo config (wrangler `account_id`) and keep only the token in the secret store.
- Create through the API with `POST /accounts/<account_id>/tokens` and the body below. The caller needs a token with Account API Tokens Edit, so the first token is always a dashboard bootstrap.

Permission-group IDs, from Tobias's dashboard export on 2026-10-06:

| ID | Permission |
|---|---|
| `1e13c5124ca64b72b1969a67e8829049` | Access: Apps and Policies Write |
| `e086da7e2179491d91ee5f35b3ca210a` | Workers Scripts Write |
| `c1fde68c7bcc44588cbb6ddbc16d6480` | Account Settings Read |

CanineArchive's GitHub deploy token, which covers Workers deploys plus a Cloudflare Access app and policy:

```json
{
  "name": "github-deploy",
  "policies": [
    {
      "effect": "allow",
      "permission_groups": [
        { "id": "1e13c5124ca64b72b1969a67e8829049" },
        { "id": "e086da7e2179491d91ee5f35b3ca210a" },
        { "id": "c1fde68c7bcc44588cbb6ddbc16d6480" }
      ],
      "resources": { "com.cloudflare.api.account.b86b55f708cb32721527d21ace6e1570": "*" }
    }
  ]
}
```

## Terraform for tokens

Use Terraform for a token only when the project already manages Cloudflare in Terraform with encrypted remote state. Otherwise keep the policy body in the repo and create the token once.

- Creating a token needs another token with API Tokens Edit, so Terraform moves the bootstrap one level up instead of removing it.
- `cloudflare_account_token` stores the token value in state, which turns the state file into a secret that needs its own storage.
- Adding Terraform for one resource beside a repo's own infra CLI splits ownership of the hosted setup.
