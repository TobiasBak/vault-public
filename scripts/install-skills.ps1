# Link every skills/<name>/ into each agent skill directory.
# Default target ~/.agents/skills serves Codex and Pi; add Claude Code's directory if it isn't linked to it.
# Override with $env:SKILLS_TARGETS = "dir1;dir2". Without -Fix, mismatches are errors.
param([switch]$Fix)
$ErrorActionPreference = "Stop"

$SkillsRoot = (Resolve-Path (Join-Path $PSScriptRoot "../skills")).Path
$Targets = if ($env:SKILLS_TARGETS) { $env:SKILLS_TARGETS -split ";" } else {
    @(Join-Path $HOME ".agents/skills")
}
$Skills = @(Get-ChildItem -Directory -LiteralPath $SkillsRoot | Where-Object { Test-Path (Join-Path $_.FullName "SKILL.md") })

function Get-LinkTarget($Path) {
    $Item = Get-Item -LiteralPath $Path -Force -ErrorAction SilentlyContinue
    if ($Item -and $Item.LinkType) { return [System.IO.Path]::GetFullPath(($Item.Target -join ";")) }
    return $null
}

foreach ($TargetDir in $Targets) {
    New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null
    foreach ($Skill in $Skills) {
        $Target = Join-Path $TargetDir $Skill.Name
        if ((Get-LinkTarget $Target) -eq [System.IO.Path]::GetFullPath($Skill.FullName)) { Write-Host "OK: $Target"; continue }
        if (Test-Path -LiteralPath $Target) {
            if (!$Fix) { throw "Wrong or unmanaged entry: $Target. Re-run with -Fix." }
            Remove-Item -LiteralPath $Target -Recurse -Force
        }
        try { New-Item -ItemType SymbolicLink -Path $Target -Target $Skill.FullName | Out-Null }
        catch { New-Item -ItemType Junction -Path $Target -Target $Skill.FullName | Out-Null }
        Write-Host "Linked: $Target -> $($Skill.FullName)"
    }
    Get-ChildItem -Force -LiteralPath $TargetDir | ForEach-Object {
        $LinkTarget = Get-LinkTarget $_.FullName
        if ($LinkTarget -and $LinkTarget.StartsWith($SkillsRoot, [System.StringComparison]::OrdinalIgnoreCase) -and
            !(Test-Path (Join-Path $LinkTarget "SKILL.md"))) {
            if (!$Fix) { throw "Stale link: $($_.FullName). Re-run with -Fix." }
            Remove-Item -LiteralPath $_.FullName -Force
            Write-Host "Removed stale: $($_.FullName)"
        }
    }
}
