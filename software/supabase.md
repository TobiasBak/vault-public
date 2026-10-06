# Supabase

## CLI

- Supabase CLI 2.116 (October 2026) runs `config push` through its TypeScript port, which reads `supabase/config.toml` from the current directory and ignores `--workdir`. It validates every `[remotes.*]` `project_id` against `^[a-z]{20}$`, so placeholder ids in the repository config fail with "Invalid config for remotes.<name>.project_id" even when `--workdir` points at a rendered config. Run hosted commands with the rendered workdir as cwd.
- Reproduce config validation without risk using a dummy `SUPABASE_ACCESS_TOKEN`: validation runs before the first API call, which then fails with 401.

## Plans

- Free-plan projects pause after a week of inactivity, and paused projects fail deploys. Restore one through the Management API with `POST /v1/projects/<ref>/restore`; no dashboard step is needed.
