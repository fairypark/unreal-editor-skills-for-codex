[CmdletBinding()]
param(
    [ValidateSet("Hook", "Enable", "Disable", "Status", "Summary", "Delete", "Feedback")]
    [string]$Action = "Hook",
    [Nullable[int]]$Rating
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version 3.0

$script:ConsentVersion = 1
$script:RetentionDays = 90
$script:MaxEvents = 10000
$script:PluginName = "unreal-editor-skills-for-codex"

function Get-MetricsRoot {
    if (-not [string]::IsNullOrWhiteSpace($env:UNREAL_CODEX_METRICS_HOME)) {
        return [System.IO.Path]::GetFullPath($env:UNREAL_CODEX_METRICS_HOME)
    }

    $localData = [Environment]::GetFolderPath([Environment+SpecialFolder]::LocalApplicationData)
    if ([string]::IsNullOrWhiteSpace($localData)) {
        $profile = [Environment]::GetFolderPath([Environment+SpecialFolder]::UserProfile)
        $localData = Join-Path $profile "AppData\Local"
    }
    return Join-Path $localData "Codex\plugin-data\$($script:PluginName)"
}

function Get-SettingsPath {
    return Join-Path (Get-MetricsRoot) "settings.json"
}

function Get-EventsPath {
    return Join-Path (Get-MetricsRoot) "events.jsonl"
}

function Get-UtcTimestamp {
    return [DateTimeOffset]::UtcNow.ToString("o")
}

function Get-PluginVersion {
    try {
        $manifestPath = Join-Path (Split-Path -Parent $PSScriptRoot) ".codex-plugin\plugin.json"
        $manifest = Get-Content -Raw -LiteralPath $manifestPath | ConvertFrom-Json
        return [string]$manifest.version
    }
    catch {
        return "unknown"
    }
}

function New-RandomSalt {
    $bytes = New-Object byte[] 32
    $generator = [Security.Cryptography.RandomNumberGenerator]::Create()
    try {
        $generator.GetBytes($bytes)
    }
    finally {
        $generator.Dispose()
    }
    return [Convert]::ToBase64String($bytes)
}

function Get-Settings {
    $path = Get-SettingsPath
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        return $null
    }
    try {
        return Get-Content -Raw -LiteralPath $path | ConvertFrom-Json
    }
    catch {
        return $null
    }
}

function Set-Settings {
    param([Parameter(Mandatory = $true)]$Settings)

    $root = Get-MetricsRoot
    [System.IO.Directory]::CreateDirectory($root) | Out-Null
    $path = Get-SettingsPath
    $temporaryPath = Join-Path $root ("settings.{0}.tmp" -f [Guid]::NewGuid().ToString("N"))
    $json = $Settings | ConvertTo-Json -Depth 8
    [System.IO.File]::WriteAllText($temporaryPath, $json, [Text.UTF8Encoding]::new($false))
    Move-Item -LiteralPath $temporaryPath -Destination $path -Force
}

function Set-ConsentStatus {
    param(
        [Parameter(Mandatory = $true)]
        [ValidateSet("enabled", "disabled")]
        [string]$Status
    )

    $settings = Get-Settings
    if ($null -eq $settings) {
        $settings = [ordered]@{
            consent_version = $script:ConsentVersion
            status = $Status
            collection = "local_only"
            decided_at = Get-UtcTimestamp
            installation_id = [Guid]::NewGuid().ToString("N")
            salt = New-RandomSalt
            retention_days = $script:RetentionDays
        }
    }
    else {
        $settings.consent_version = $script:ConsentVersion
        $settings.status = $Status
        $settings.collection = "local_only"
        $settings.decided_at = Get-UtcTimestamp
        if ($null -eq $settings.PSObject.Properties["salt"]) {
            $settings | Add-Member -NotePropertyName salt -NotePropertyValue (New-RandomSalt)
        }
        if ($null -eq $settings.PSObject.Properties["installation_id"]) {
            $settings | Add-Member -NotePropertyName installation_id -NotePropertyValue ([Guid]::NewGuid().ToString("N"))
        }
        if ($null -eq $settings.PSObject.Properties["retention_days"]) {
            $settings | Add-Member -NotePropertyName retention_days -NotePropertyValue $script:RetentionDays
        }
    }

    Set-Settings -Settings $settings
    return $settings
}

function Get-AnonymousId {
    param(
        [AllowNull()][string]$Value,
        [Parameter(Mandatory = $true)][string]$Salt
    )

    if ([string]::IsNullOrWhiteSpace($Value)) {
        return $null
    }

    $bytes = [Text.Encoding]::UTF8.GetBytes("$Salt`n$Value")
    $hashAlgorithm = [Security.Cryptography.SHA256]::Create()
    try {
        $hash = $hashAlgorithm.ComputeHash($bytes)
    }
    finally {
        $hashAlgorithm.Dispose()
    }
    return ([BitConverter]::ToString($hash).Replace("-", "").ToLowerInvariant()).Substring(0, 24)
}

function Get-PropertyValue {
    param(
        [AllowNull()]$Object,
        [Parameter(Mandatory = $true)][string]$Name
    )

    if ($null -eq $Object) {
        return $null
    }
    if ($Object -is [System.Collections.IDictionary]) {
        foreach ($key in $Object.Keys) {
            if ([string]$key -ieq $Name) {
                return $Object[$key]
            }
        }
        return $null
    }

    $property = $Object.PSObject.Properties |
        Where-Object { $_.Name -ieq $Name } |
        Select-Object -First 1
    if ($null -eq $property) {
        return $null
    }
    return $property.Value
}

function ConvertTo-SafeIdentifier {
    param([AllowNull()]$Value)

    if ($null -eq $Value) {
        return $null
    }
    $text = [string]$Value
    if ($text.Length -gt 128) {
        $text = $text.Substring(0, 128)
    }
    return [Regex]::Replace($text, "[^A-Za-z0-9_.:-]", "_")
}

function Write-Event {
    param([Parameter(Mandatory = $true)]$Event)

    $root = Get-MetricsRoot
    [System.IO.Directory]::CreateDirectory($root) | Out-Null
    $line = ($Event | ConvertTo-Json -Depth 8 -Compress) + [Environment]::NewLine
    $path = Get-EventsPath

    for ($attempt = 0; $attempt -lt 5; $attempt++) {
        try {
            $stream = [System.IO.FileStream]::new(
                $path,
                [System.IO.FileMode]::Append,
                [System.IO.FileAccess]::Write,
                [System.IO.FileShare]::Read
            )
            try {
                $writer = [System.IO.StreamWriter]::new($stream, [Text.UTF8Encoding]::new($false))
                try {
                    $writer.Write($line)
                    $writer.Flush()
                }
                finally {
                    $writer.Dispose()
                }
            }
            finally {
                $stream.Dispose()
            }
            return
        }
        catch [System.IO.IOException] {
            if ($attempt -eq 4) {
                throw
            }
            Start-Sleep -Milliseconds (20 * ($attempt + 1))
        }
    }
}

function Get-Events {
    $path = Get-EventsPath
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        return @()
    }

    $events = [System.Collections.Generic.List[object]]::new()
    foreach ($line in [System.IO.File]::ReadLines($path)) {
        if ([string]::IsNullOrWhiteSpace($line)) {
            continue
        }
        try {
            $events.Add(($line | ConvertFrom-Json))
        }
        catch {
            continue
        }
    }
    return @($events)
}

function Trim-Events {
    $path = Get-EventsPath
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        return
    }

    $cutoff = [DateTimeOffset]::UtcNow.AddDays(-$script:RetentionDays)
    $kept = [System.Collections.Generic.List[object]]::new()
    foreach ($event in (Get-Events)) {
        try {
            $timestamp = [DateTimeOffset]::Parse([string]$event.timestamp)
            if ($timestamp -ge $cutoff) {
                $kept.Add($event)
            }
        }
        catch {
            continue
        }
    }

    if ($kept.Count -gt $script:MaxEvents) {
        $kept = [System.Collections.Generic.List[object]]::new(
            [object[]]($kept | Select-Object -Last $script:MaxEvents)
        )
    }

    $content = if ($kept.Count -eq 0) {
        ""
    }
    else {
        (($kept | ForEach-Object { $_ | ConvertTo-Json -Depth 8 -Compress }) -join [Environment]::NewLine) +
            [Environment]::NewLine
    }
    [System.IO.File]::WriteAllText($path, $content, [Text.UTF8Encoding]::new($false))
}

function Test-UnrealProjectRoot {
    param([Parameter(Mandatory = $true)][string]$Directory)

    foreach ($marker in @("GenerateProjectFiles.bat", "GenerateProjectFiles.sh", "GenerateProjectFiles.command")) {
        if (Test-Path -LiteralPath (Join-Path $Directory $marker) -PathType Leaf) {
            return $true
        }
    }
    return $null -ne (Get-ChildItem -LiteralPath $Directory -Filter "*.uproject" -File -ErrorAction SilentlyContinue |
        Select-Object -First 1)
}

function Test-InUnrealProject {
    param([AllowNull()][string]$StartDirectory)

    if ([string]::IsNullOrWhiteSpace($StartDirectory) -or -not (Test-Path -LiteralPath $StartDirectory -PathType Container)) {
        return $false
    }
    $current = [System.IO.DirectoryInfo]::new($StartDirectory)
    while ($null -ne $current) {
        if (Test-UnrealProjectRoot -Directory $current.FullName) {
            return $true
        }
        $current = $current.Parent
    }
    return $false
}

function New-BaseEvent {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [AllowNull()]$HookInput,
        [Parameter(Mandatory = $true)]$Settings
    )

    $sessionId = Get-PropertyValue -Object $HookInput -Name "session_id"
    $turnId = Get-PropertyValue -Object $HookInput -Name "turn_id"
    return [ordered]@{
        schema_version = 1
        event = $Name
        timestamp = Get-UtcTimestamp
        plugin_version = Get-PluginVersion
        session_id = Get-AnonymousId -Value ([string]$sessionId) -Salt ([string]$Settings.salt)
        turn_id = Get-AnonymousId -Value ([string]$turnId) -Salt ([string]$Settings.salt)
    }
}

function Get-MetaToolName {
    param([AllowNull()]$ToolName)

    if ($null -eq $ToolName) {
        return $null
    }
    $parts = ([string]$ToolName) -split "__"
    return ConvertTo-SafeIdentifier -Value $parts[-1]
}

function Get-OperationClass {
    param(
        [AllowNull()][string]$MetaTool,
        [AllowNull()][string]$DispatchedTool
    )

    if ($MetaTool -in @("list_toolsets", "describe_toolset")) {
        return "discovery"
    }
    if ([string]::IsNullOrWhiteSpace($DispatchedTool)) {
        return "unknown"
    }
    if ($DispatchedTool -match "^(Compile|Test|Validate|Verify|Check|Run.*Test)") {
        return "verification"
    }
    if ($DispatchedTool -match "^(Create|Add|Set|Update|Delete|Remove|Move|Rename|Duplicate|Import|Export|Save|Spawn|Destroy|Execute|Start|Stop|Apply|Build)") {
        return "mutation"
    }
    return "read"
}

function Test-ExplicitFailure {
    param(
        [AllowNull()]$Value,
        [int]$Depth = 0
    )

    if ($null -eq $Value -or $Depth -gt 5 -or $Value -is [string] -or $Value.GetType().IsPrimitive) {
        return $false
    }

    foreach ($name in @("isError", "success", "ok", "status")) {
        $propertyValue = Get-PropertyValue -Object $Value -Name $name
        if ($null -eq $propertyValue) {
            continue
        }
        if ($name -ieq "isError" -and $propertyValue -eq $true) {
            return $true
        }
        if ($name -in @("success", "ok") -and $propertyValue -eq $false) {
            return $true
        }
        if ($name -ieq "status" -and ([string]$propertyValue).ToLowerInvariant() -in @("error", "failed", "failure")) {
            return $true
        }
    }

    if ($Value -is [System.Collections.IDictionary]) {
        foreach ($entry in $Value.Values) {
            if (Test-ExplicitFailure -Value $entry -Depth ($Depth + 1)) {
                return $true
            }
        }
    }
    elseif ($Value -is [System.Collections.IEnumerable]) {
        foreach ($entry in $Value) {
            if (Test-ExplicitFailure -Value $entry -Depth ($Depth + 1)) {
                return $true
            }
        }
    }
    else {
        foreach ($property in $Value.PSObject.Properties) {
            if (Test-ExplicitFailure -Value $property.Value -Depth ($Depth + 1)) {
                return $true
            }
        }
    }
    return $false
}

function Add-ToolEvent {
    param(
        [Parameter(Mandatory = $true)]$HookInput,
        [Parameter(Mandatory = $true)]$Settings,
        [Parameter(Mandatory = $true)]
        [ValidateSet("tool_started", "tool_finished")]
        [string]$EventName
    )

    $toolName = [string](Get-PropertyValue -Object $HookInput -Name "tool_name")
    if ($toolName -notmatch "^mcp__unreal[-_]mcp__.*$") {
        return
    }

    $toolInput = Get-PropertyValue -Object $HookInput -Name "tool_input"
    $metaTool = Get-MetaToolName -ToolName $toolName
    $toolsetName = ConvertTo-SafeIdentifier -Value (Get-PropertyValue -Object $toolInput -Name "toolset_name")
    $dispatchedTool = ConvertTo-SafeIdentifier -Value (Get-PropertyValue -Object $toolInput -Name "tool_name")
    $toolUseId = [string](Get-PropertyValue -Object $HookInput -Name "tool_use_id")

    $event = New-BaseEvent -Name $EventName -HookInput $HookInput -Settings $Settings
    $event.tool_call_id = Get-AnonymousId -Value $toolUseId -Salt ([string]$Settings.salt)
    $event.meta_tool = $metaTool
    $event.toolset = $toolsetName
    $event.tool = $dispatchedTool
    $event.operation = Get-OperationClass -MetaTool $metaTool -DispatchedTool $dispatchedTool

    if ($EventName -eq "tool_finished") {
        $response = Get-PropertyValue -Object $HookInput -Name "tool_response"
        $event.outcome = if (Test-ExplicitFailure -Value $response) { "failure" } else { "success" }
    }
    Write-Event -Event $event
}

function Add-TurnSummary {
    param(
        [Parameter(Mandatory = $true)]$HookInput,
        [Parameter(Mandatory = $true)]$Settings
    )

    $turnId = [string](Get-PropertyValue -Object $HookInput -Name "turn_id")
    $turnHash = Get-AnonymousId -Value $turnId -Salt ([string]$Settings.salt)
    if ([string]::IsNullOrWhiteSpace($turnHash)) {
        return
    }

    $events = @(Get-Events | Where-Object { $_.turn_id -eq $turnHash })
    if ($events | Where-Object { $_.event -eq "turn_summary" }) {
        return
    }
    $finished = @($events | Where-Object { $_.event -eq "tool_finished" } | Sort-Object timestamp)
    if ($finished.Count -eq 0) {
        return
    }

    $failures = @($finished | Where-Object { $_.outcome -eq "failure" }).Count
    $mutations = @($finished | Where-Object { $_.operation -eq "mutation" })
    $verificationAfterMutation = $false
    $mutationSeen = $false
    foreach ($event in $finished) {
        if ($event.operation -eq "mutation") {
            $mutationSeen = $true
            continue
        }
        if ($mutationSeen -and $event.operation -in @("read", "verification")) {
            $verificationAfterMutation = $true
            break
        }
    }

    $retries = 0
    $groups = $finished | Group-Object { "{0}|{1}|{2}" -f $_.meta_tool, $_.toolset, $_.tool }
    foreach ($group in $groups) {
        if ($group.Count -gt 1) {
            $retries += $group.Count - 1
        }
    }

    $started = @($events | Where-Object { $_.event -eq "tool_started" } | Sort-Object timestamp)
    $durationMs = $null
    if ($started.Count -gt 0) {
        try {
            $startTime = [DateTimeOffset]::Parse([string]$started[0].timestamp)
            $endTime = [DateTimeOffset]::Parse([string]$finished[-1].timestamp)
            $durationMs = [Math]::Max(0, [Math]::Round(($endTime - $startTime).TotalMilliseconds))
        }
        catch {
            $durationMs = $null
        }
    }

    $summary = New-BaseEvent -Name "turn_summary" -HookInput $HookInput -Settings $Settings
    $summary.tool_calls = $finished.Count
    $summary.failures = $failures
    $summary.retry_count = $retries
    $summary.mutation_calls = $mutations.Count
    $summary.verification_after_mutation = $verificationAfterMutation
    $summary.duration_ms = $durationMs
    $summary.outcome = if ($failures -eq 0) { "success" } else { "failure" }
    Write-Event -Event $summary
}

function Write-ConsentContext {
    $context = @(
        "The optional local usage-metrics preference for Unreal Editor Skills for Codex is not set."
        "Complete the user's current task without collecting metrics, then ask once in the user's language whether to enable local-only anonymous usage metrics."
        "Explain that prompts, responses, file paths, project names, Actor or Asset names, tool arguments, and tool response contents are never stored."
        "Say that metrics can be enabled, disabled, summarized, or deleted at any time."
        "After the user chooses, use the ``unreal-usage-metrics`` skill to save either enabled or disabled."
        "Do not block or delay the current task for this question."
    ) -join " "

    @{
        hookSpecificOutput = @{
            hookEventName = "SessionStart"
            additionalContext = $context
        }
    } | ConvertTo-Json -Depth 4 -Compress
}

function Invoke-Hook {
    $raw = [Console]::In.ReadToEnd()
    if ([string]::IsNullOrWhiteSpace($raw)) {
        return
    }
    $hookInput = $raw | ConvertFrom-Json
    $eventName = [string](Get-PropertyValue -Object $hookInput -Name "hook_event_name")
    $settings = Get-Settings

    if ($eventName -eq "SessionStart") {
        $cwd = [string](Get-PropertyValue -Object $hookInput -Name "cwd")
        if (-not (Test-InUnrealProject -StartDirectory $cwd)) {
            return
        }
        $storedConsentVersion = Get-PropertyValue -Object $settings -Name "consent_version"
        if ($null -eq $settings -or $null -eq $storedConsentVersion -or [int]$storedConsentVersion -ne $script:ConsentVersion) {
            Write-ConsentContext
            return
        }
        if ([string]$settings.status -ne "enabled") {
            return
        }
        Trim-Events
        $event = New-BaseEvent -Name "session_eligible" -HookInput $hookInput -Settings $settings
        $event.source = ConvertTo-SafeIdentifier -Value (Get-PropertyValue -Object $hookInput -Name "source")
        Write-Event -Event $event
        return
    }

    if ($eventName -eq "Stop") {
        if ($null -ne $settings -and [string]$settings.status -eq "enabled") {
            Add-TurnSummary -HookInput $hookInput -Settings $settings
        }
        Write-Output "{}"
        return
    }

    if ($null -eq $settings -or [string]$settings.status -ne "enabled") {
        return
    }
    if ($eventName -eq "PreToolUse") {
        Add-ToolEvent -HookInput $hookInput -Settings $settings -EventName "tool_started"
    }
    elseif ($eventName -eq "PostToolUse") {
        Add-ToolEvent -HookInput $hookInput -Settings $settings -EventName "tool_finished"
    }
}

function Get-MetricsSummary {
    $events = @(Get-Events)
    $eligibleSessions = @($events | Where-Object { $_.event -eq "session_eligible" } |
        Select-Object -ExpandProperty session_id -Unique)
    $toolEvents = @($events | Where-Object { $_.event -eq "tool_finished" })
    $activeSessions = @($toolEvents | Select-Object -ExpandProperty session_id -Unique)
    $turns = @($events | Where-Object { $_.event -eq "turn_summary" })
    $mutationTurns = @($turns | Where-Object { [int]$_.mutation_calls -gt 0 })
    $verifiedMutationTurns = @($mutationTurns | Where-Object { $_.verification_after_mutation -eq $true })
    $feedback = @($events | Where-Object { $_.event -eq "user_feedback" })

    $successRate = if ($toolEvents.Count -eq 0) {
        $null
    }
    else {
        [Math]::Round(100 * @($toolEvents | Where-Object { $_.outcome -eq "success" }).Count / $toolEvents.Count, 1)
    }
    $activationRate = if ($eligibleSessions.Count -eq 0) {
        $null
    }
    else {
        [Math]::Round(100 * $activeSessions.Count / $eligibleSessions.Count, 1)
    }
    $verificationRate = if ($mutationTurns.Count -eq 0) {
        $null
    }
    else {
        [Math]::Round(100 * $verifiedMutationTurns.Count / $mutationTurns.Count, 1)
    }
    $averageRating = if ($feedback.Count -eq 0) {
        $null
    }
    else {
        [Math]::Round(($feedback | Measure-Object -Property rating -Average).Average, 2)
    }

    return [ordered]@{
        collection = "local_only"
        retention_days = $script:RetentionDays
        eligible_sessions = $eligibleSessions.Count
        active_sessions = $activeSessions.Count
        activation_rate_percent = $activationRate
        turns_with_unreal_tools = $turns.Count
        tool_calls = $toolEvents.Count
        tool_success_rate_percent = $successRate
        mutation_turns = $mutationTurns.Count
        verified_mutation_turns = $verifiedMutationTurns.Count
        verification_rate_percent = $verificationRate
        feedback_count = $feedback.Count
        average_feedback_rating = $averageRating
    }
}

try {
    switch ($Action) {
        "Enable" {
            Set-ConsentStatus -Status "enabled" | Out-Null
            [ordered]@{
                status = "enabled"
                collection = "local_only"
                message = "Optional local usage metrics are enabled."
            } | ConvertTo-Json -Compress
        }
        "Disable" {
            Set-ConsentStatus -Status "disabled" | Out-Null
            [ordered]@{
                status = "disabled"
                existing_data_retained = Test-Path -LiteralPath (Get-EventsPath)
                message = "New usage-metrics collection is disabled. Existing data was not deleted."
            } | ConvertTo-Json -Compress
        }
        "Status" {
            $settings = Get-Settings
            [ordered]@{
                status = if ($null -eq $settings) { "unset" } else { [string]$settings.status }
                consent_version = if ($null -eq $settings) { $null } else { [int]$settings.consent_version }
                collection = "local_only"
                data_location = Get-MetricsRoot
                data_exists = Test-Path -LiteralPath (Get-EventsPath)
            } | ConvertTo-Json -Compress
        }
        "Summary" {
            Get-MetricsSummary | ConvertTo-Json -Depth 6 -Compress
        }
        "Delete" {
            $eventsPath = Get-EventsPath
            if (Test-Path -LiteralPath $eventsPath -PathType Leaf) {
                Remove-Item -LiteralPath $eventsPath -Force
            }
            [ordered]@{
                deleted = $true
                preference_retained = $true
                message = "Stored usage-metrics events were deleted. The current preference was retained."
            } | ConvertTo-Json -Compress
        }
        "Feedback" {
            if ($null -eq $Rating -or $Rating -lt 1 -or $Rating -gt 5) {
                throw "Feedback requires -Rating from 1 to 5."
            }
            $settings = Get-Settings
            if ($null -eq $settings -or [string]$settings.status -ne "enabled") {
                throw "Usage metrics are not enabled."
            }
            $event = New-BaseEvent -Name "user_feedback" -HookInput $null -Settings $settings
            $event.rating = [int]$Rating
            Write-Event -Event $event
            [ordered]@{
                recorded = $true
                rating = [int]$Rating
                message = "The local rating was recorded."
            } | ConvertTo-Json -Compress
        }
        "Hook" {
            Invoke-Hook
        }
    }
}
catch {
    if ($Action -eq "Hook") {
        try {
            if ($null -ne $hookInput -and [string](Get-PropertyValue -Object $hookInput -Name "hook_event_name") -eq "Stop") {
                Write-Output "{}"
            }
        }
        catch {
        }
        exit 0
    }
    [ordered]@{
        error = $_.Exception.Message
    } | ConvertTo-Json -Compress
    exit 1
}
