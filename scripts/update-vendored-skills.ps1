# Refresh Matt Pocock's vendored skills, keeping upstream content except invocation metadata.
# Keeps each skill's local agents/openai.yaml, enables model discovery, and copies LICENSE in.
# Refuses to overwrite uncommitted changes unless -Force.
param([switch]$Force)
$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Upstream = [ordered]@{
    "domain-modeling" = "skills/engineering/domain-modeling"
    "grill-with-docs" = "skills/engineering/grill-with-docs"
    "grilling"        = "skills/productivity/grilling"
}
$Paths = @($Upstream.Keys | ForEach-Object { "skills/$_" })

function Invoke-Git { & git @args; if ($LASTEXITCODE -ne 0) { throw "git $args failed" } }

if (!$Force) {
    $Pending = @(Invoke-Git -C $RepoRoot status --short -- @Paths)
    if ($Pending.Count -gt 0) { throw "Uncommitted changes in vendored skills:`n$($Pending -join "`n")" }
}

$Tmp = Join-Path ([System.IO.Path]::GetTempPath()) ("skills-" + [guid]::NewGuid())
try {
    $Repo = Join-Path $Tmp "repo"
    Invoke-Git clone -q --depth 1 --filter=blob:none --sparse https://github.com/mattpocock/skills $Repo
    Invoke-Git -C $Repo sparse-checkout set --no-cone /LICENSE @($Upstream.Values | ForEach-Object { "/$_" })
    foreach ($Name in $Upstream.Keys) {
        $Src = Join-Path $Repo $Upstream[$Name]
        if (!(Test-Path (Join-Path $Src "SKILL.md"))) { throw "Missing upstream: $($Upstream[$Name])" }
        $Dest = Join-Path $RepoRoot "skills/$Name"
        $Meta = Join-Path $Dest "agents/openai.yaml"
        $SavedMeta = Join-Path $Tmp "$Name.openai.yaml"
        if (Test-Path $Meta) { Copy-Item $Meta $SavedMeta }
        if (Test-Path $Dest) { Remove-Item -Recurse -Force $Dest }
        Copy-Item -Recurse $Src $Dest
        Copy-Item (Join-Path $Repo "LICENSE") (Join-Path $Dest "LICENSE")
        $SkillPath = Join-Path $Dest "SKILL.md"
        $Content = [System.IO.File]::ReadAllText($SkillPath)
        $Content = [regex]::Replace($Content, '(?m)^disable-model-invocation:[^\r\n]*(?:\r?\n|$)', '')
        [System.IO.File]::WriteAllText($SkillPath, $Content, [System.Text.UTF8Encoding]::new($false))
        if (Test-Path $SavedMeta) {
            New-Item -ItemType Directory -Force (Split-Path $Meta) | Out-Null
            Copy-Item $SavedMeta $Meta
        }
    }
    Write-Host "Updated from mattpocock/skills@$(Invoke-Git -C $Repo rev-parse --short HEAD). Review:"
    Invoke-Git -C $RepoRoot status --short -- @Paths
} finally {
    Remove-Item -Recurse -Force $Tmp -ErrorAction SilentlyContinue
}
