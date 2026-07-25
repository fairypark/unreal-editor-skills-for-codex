$ErrorActionPreference = "Stop"

function Test-UnrealProjectRoot {
    param([Parameter(Mandatory = $true)][string]$Directory)

    if (Test-Path -LiteralPath (Join-Path $Directory "GenerateProjectFiles.bat") -PathType Leaf) {
        return $true
    }
    if (Test-Path -LiteralPath (Join-Path $Directory "GenerateProjectFiles.sh") -PathType Leaf) {
        return $true
    }
    if (Test-Path -LiteralPath (Join-Path $Directory "GenerateProjectFiles.command") -PathType Leaf) {
        return $true
    }
    return $null -ne (Get-ChildItem -LiteralPath $Directory -Filter "*.uproject" -File -ErrorAction SilentlyContinue | Select-Object -First 1)
}

function Find-UnrealProjectRoot {
    param([Parameter(Mandatory = $true)][string]$StartDirectory)

    $current = [System.IO.DirectoryInfo]::new($StartDirectory)
    while ($null -ne $current) {
        if (Test-UnrealProjectRoot -Directory $current.FullName) {
            return $current.FullName
        }
        $current = $current.Parent
    }
    return $null
}

$projectRoot = Find-UnrealProjectRoot -StartDirectory (Get-Location).Path
if ([string]::IsNullOrWhiteSpace($projectRoot)) {
    exit 0
}

$isEngineSource = Test-Path -LiteralPath (Join-Path $projectRoot "Engine") -PathType Container
$uproject = Get-ChildItem -LiteralPath $projectRoot -Filter "*.uproject" -File -ErrorAction SilentlyContinue | Select-Object -First 1
$codexConfig = Join-Path $projectRoot ".codex\config.toml"

$parts = [System.Collections.Generic.List[string]]::new()
$parts.Add("This working directory is an Unreal Engine project.")
if ($isEngineSource) {
    $parts.Add("It is an Engine source tree.")
}
elseif ($null -ne $uproject) {
    $parts.Add("The project is ``$($uproject.Name)``.")
}
$parts.Add("Prefer Unreal Engine conventions, including UObject patterns, UHT reflection, Slate, and project-local naming rules.")
$parts.Add("Use the ``unreal-mcp`` skill for tasks that inspect or mutate the live Unreal Editor.")
$parts.Add("Serialize Unreal MCP calls, save before bulk mutations, and verify every tool result.")
if (Test-Path -LiteralPath $codexConfig -PathType Leaf) {
    $parts.Add("A project-scoped ``.codex/config.toml`` is present.")
}
else {
    $parts.Add("No project-scoped ``.codex/config.toml`` was detected; this plugin can still supply its bundled ``unreal-mcp`` connection.")
}

$payload = @{
    hookSpecificOutput = @{
        hookEventName = "SessionStart"
        additionalContext = ($parts -join " ")
    }
}

$payload | ConvertTo-Json -Depth 4 -Compress
