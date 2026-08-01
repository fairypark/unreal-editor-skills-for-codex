[CmdletBinding()]
param(
    [ValidateSet("Hook", "Enable", "Disable", "Status", "Summary", "Delete", "Feedback")]
    [string]$Action = "Hook",
    [Nullable[int]]$Rating,
    [ValidateSet("all", "UnrealToolsetsExtension")]
    [string]$Target = "all",
    [switch]$Shareable
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version 3.0

$script:ConsentVersion = 2
$script:RetentionDays = 90
$script:MaxEvents = 10000
$script:PluginName = "unreal-editor-skills-for-codex"
$script:ExtensionName = "UnrealToolsetsExtension"
$script:ExtensionCatalog = $null

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

function Get-ExtensionCatalog {
    if ($null -ne $script:ExtensionCatalog) {
        return $script:ExtensionCatalog
    }

    $path = Join-Path $PSScriptRoot "unreal-toolsets-extension-catalog.json"
    try {
        $script:ExtensionCatalog = Get-Content -Raw -LiteralPath $path | ConvertFrom-Json
    }
    catch {
        $script:ExtensionCatalog = $null
    }
    return $script:ExtensionCatalog
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

function Set-PropertyValue {
    param(
        [Parameter(Mandatory = $true)]$Object,
        [Parameter(Mandatory = $true)][string]$Name,
        [AllowNull()]$Value
    )

    if ($Object -is [System.Collections.IDictionary]) {
        $Object[$Name] = $Value
        return
    }
    $property = $Object.PSObject.Properties |
        Where-Object { $_.Name -ieq $Name } |
        Select-Object -First 1
    if ($null -eq $property) {
        $Object | Add-Member -NotePropertyName $Name -NotePropertyValue $Value
    }
    else {
        $property.Value = $Value
    }
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

function Update-ObservedExtensionInfo {
    param(
        [Parameter(Mandatory = $true)]$Settings,
        [AllowNull()]$Response
    )

    $version = Find-PropertyValue -Value $Response -Names @("extension_version", "ExtensionVersion")
    $engineVersion = Find-PropertyValue -Value $Response -Names @("engine_version", "EngineVersion")
    $contractVersion = Find-PropertyValue -Value $Response -Names @(
        "observability_contract_version",
        "ObservabilityContractVersion"
    )
    if ($null -ne $version) {
        Set-PropertyValue -Object $Settings -Name "observed_extension_version" -Value (
            ConvertTo-SafeIdentifier -Value $version
        )
    }
    if ($null -ne $engineVersion) {
        Set-PropertyValue -Object $Settings -Name "observed_engine_version" -Value (
            ConvertTo-SafeIdentifier -Value $engineVersion
        )
    }
    if ($null -ne $contractVersion -and [int]$contractVersion -ge 1) {
        Set-PropertyValue -Object $Settings -Name "observed_extension_contract_version" -Value (
            [int]$contractVersion
        )
    }
    Set-Settings -Settings $Settings
    return $Settings
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

function Find-PropertyValue {
    param(
        [AllowNull()]$Value,
        [Parameter(Mandatory = $true)][string[]]$Names,
        [int]$Depth = 0
    )

    if ($null -eq $Value -or $Depth -gt 6) {
        return $null
    }

    foreach ($name in $Names) {
        $candidate = Get-PropertyValue -Object $Value -Name $name
        if ($null -ne $candidate) {
            return $candidate
        }
    }

    if ($Value -is [string]) {
        $text = [string]$Value
        if ($text.Length -le 1048576 -and $text.TrimStart().StartsWith("{")) {
            try {
                return Find-PropertyValue -Value ($text | ConvertFrom-Json) -Names $Names -Depth ($Depth + 1)
            }
            catch {
                return $null
            }
        }
        return $null
    }
    if ($Value.GetType().IsPrimitive) {
        return $null
    }

    if ($Value -is [System.Collections.IDictionary]) {
        foreach ($entry in $Value.Values) {
            $found = Find-PropertyValue -Value $entry -Names $Names -Depth ($Depth + 1)
            if ($null -ne $found) {
                return $found
            }
        }
    }
    elseif ($Value -is [System.Collections.IEnumerable]) {
        foreach ($entry in $Value) {
            $found = Find-PropertyValue -Value $entry -Names $Names -Depth ($Depth + 1)
            if ($null -ne $found) {
                return $found
            }
        }
    }
    else {
        foreach ($property in $Value.PSObject.Properties) {
            $found = Find-PropertyValue -Value $property.Value -Names $Names -Depth ($Depth + 1)
            if ($null -ne $found) {
                return $found
            }
        }
    }
    return $null
}

function Test-ContainsExactString {
    param(
        [AllowNull()]$Value,
        [Parameter(Mandatory = $true)][System.Collections.Generic.HashSet[string]]$Allowed,
        [int]$Depth = 0
    )

    if ($null -eq $Value -or $Depth -gt 6) {
        return $false
    }
    if ($Value -is [string]) {
        $text = [string]$Value
        if ($Allowed.Contains($text)) {
            return $true
        }
        if ($text.Length -le 1048576 -and ($text.TrimStart().StartsWith("{") -or $text.TrimStart().StartsWith("["))) {
            try {
                return Test-ContainsExactString -Value ($text | ConvertFrom-Json) -Allowed $Allowed -Depth ($Depth + 1)
            }
            catch {
                return $false
            }
        }
        return $false
    }
    if ($Value.GetType().IsPrimitive) {
        return $false
    }

    if ($Value -is [System.Collections.IDictionary]) {
        foreach ($entry in $Value.Values) {
            if (Test-ContainsExactString -Value $entry -Allowed $Allowed -Depth ($Depth + 1)) {
                return $true
            }
        }
    }
    elseif ($Value -is [System.Collections.IEnumerable]) {
        foreach ($entry in $Value) {
            if (Test-ContainsExactString -Value $entry -Allowed $Allowed -Depth ($Depth + 1)) {
                return $true
            }
        }
    }
    else {
        foreach ($property in $Value.PSObject.Properties) {
            if (Test-ContainsExactString -Value $property.Value -Allowed $Allowed -Depth ($Depth + 1)) {
                return $true
            }
        }
    }
    return $false
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

function Get-ExtensionOperationDescriptor {
    param(
        [AllowNull()][string]$Toolset,
        [AllowNull()][string]$Tool
    )

    $catalog = Get-ExtensionCatalog
    if ($null -eq $catalog -or [string]::IsNullOrWhiteSpace($Toolset) -or [string]::IsNullOrWhiteSpace($Tool)) {
        return $null
    }
    return $catalog.operations |
        Where-Object {
            [string]$_.toolset -ceq $Toolset -and
            [string]$_.operation -ceq $Tool
        } |
        Select-Object -First 1
}

function Find-ExtensionErrorDescriptor {
    param(
        [AllowNull()]$Value,
        [int]$Depth = 0
    )

    if ($null -eq $Value -or $Depth -gt 6) {
        return $null
    }

    $catalog = Get-ExtensionCatalog
    if ($null -eq $catalog) {
        return $null
    }
    if ($Value -is [string]) {
        $text = [string]$Value
        foreach ($descriptor in $catalog.errors) {
            $code = [string]$descriptor.code
            if ($text -match "(?<![A-Z0-9_])$([Regex]::Escape($code))(?![A-Z0-9_])") {
                return $descriptor
            }
        }
        if ($text.Length -le 1048576 -and ($text.TrimStart().StartsWith("{") -or $text.TrimStart().StartsWith("["))) {
            try {
                return Find-ExtensionErrorDescriptor -Value ($text | ConvertFrom-Json) -Depth ($Depth + 1)
            }
            catch {
                return $null
            }
        }
        return $null
    }
    if ($Value.GetType().IsPrimitive) {
        return $null
    }

    if ($Value -is [System.Collections.IDictionary]) {
        foreach ($entry in $Value.Values) {
            $found = Find-ExtensionErrorDescriptor -Value $entry -Depth ($Depth + 1)
            if ($null -ne $found) {
                return $found
            }
        }
    }
    elseif ($Value -is [System.Collections.IEnumerable]) {
        foreach ($entry in $Value) {
            $found = Find-ExtensionErrorDescriptor -Value $entry -Depth ($Depth + 1)
            if ($null -ne $found) {
                return $found
            }
        }
    }
    else {
        foreach ($property in $Value.PSObject.Properties) {
            $found = Find-ExtensionErrorDescriptor -Value $property.Value -Depth ($Depth + 1)
            if ($null -ne $found) {
                return $found
            }
        }
    }
    return $null
}

function Add-ObservedExtensionFields {
    param(
        [Parameter(Mandatory = $true)]$Event,
        [Parameter(Mandatory = $true)]$Settings
    )

    $event.extension = $script:ExtensionName
    $event.extension_version = Get-PropertyValue -Object $Settings -Name "observed_extension_version"
    $event.engine_version = Get-PropertyValue -Object $Settings -Name "observed_engine_version"
    $observedContract = Get-PropertyValue -Object $Settings -Name "observed_extension_contract_version"
    $catalog = Get-ExtensionCatalog
    $event.extension_contract_version = if ($null -ne $observedContract) {
        [int]$observedContract
    }
    elseif ($null -ne $catalog) {
        [int]$catalog.contract_version
    }
    else {
        $null
    }
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
    $catalog = Get-ExtensionCatalog
    $isExtensionToolset = $null -ne $catalog -and @($catalog.toolsets) -ccontains $toolsetName
    $extensionDescriptor = if ($isExtensionToolset) {
        Get-ExtensionOperationDescriptor -Toolset $toolsetName -Tool $dispatchedTool
    }
    else {
        $null
    }

    $event = New-BaseEvent -Name $EventName -HookInput $HookInput -Settings $Settings
    $event.tool_call_id = Get-AnonymousId -Value $toolUseId -Salt ([string]$Settings.salt)
    $event.meta_tool = $metaTool
    $event.toolset = $toolsetName
    $event.tool = $dispatchedTool
    $event.operation = Get-OperationClass -MetaTool $metaTool -DispatchedTool $dispatchedTool
    if ($isExtensionToolset) {
        Add-ObservedExtensionFields -Event $event -Settings $Settings
        $event.extension_operation_class = if ($null -eq $extensionDescriptor) {
            "unknown"
        }
        else {
            [string]$extensionDescriptor.class
        }
        $event.extension_verification = if ($null -eq $extensionDescriptor) {
            "unknown"
        }
        else {
            [string]$extensionDescriptor.verification
        }
        $event.extension_persistence = if ($null -eq $extensionDescriptor) {
            "unknown"
        }
        else {
            [string]$extensionDescriptor.persistence
        }
        $event.extension_may_dry_run = if ($null -eq $extensionDescriptor) {
            $null
        }
        else {
            [bool]$extensionDescriptor.may_dry_run
        }
        $mayAttemptRollback = Get-PropertyValue -Object $extensionDescriptor -Name "may_attempt_rollback"
        $event.extension_may_attempt_rollback = if ($null -eq $extensionDescriptor) {
            $null
        }
        elseif ($null -eq $mayAttemptRollback) {
            $false
        }
        else {
            [bool]$mayAttemptRollback
        }
    }

    if ($EventName -eq "tool_finished") {
        $response = Get-PropertyValue -Object $HookInput -Name "tool_response"
        $event.outcome = if (Test-ExplicitFailure -Value $response) { "failure" } else { "success" }
        if ($isExtensionToolset -and
            $toolsetName -ceq "ObservabilityExtensionToolset" -and
            $dispatchedTool -ceq "GetExtensionObservabilityInfo" -and
            $event.outcome -eq "success") {
            $Settings = Update-ObservedExtensionInfo -Settings $Settings -Response $response
            Add-ObservedExtensionFields -Event $event -Settings $Settings
        }
        if ($isExtensionToolset -and $event.outcome -eq "failure") {
            $errorDescriptor = Find-ExtensionErrorDescriptor -Value $response
            if ($null -ne $errorDescriptor) {
                $event.error_code = [string]$errorDescriptor.code
                $event.failure_category = [string]$errorDescriptor.category
                $event.rollback = if ([bool]$errorDescriptor.verified_rollback) {
                    "verified"
                }
                else {
                    "none"
                }
            }
        }

        $started = @(Get-Events | Where-Object {
            $_.event -eq "tool_started" -and
            $_.tool_call_id -eq $event.tool_call_id
        } | Select-Object -Last 1)
        if ($started.Count -eq 1) {
            try {
                $startTime = [DateTimeOffset]::Parse([string]$started[0].timestamp)
                $endTime = [DateTimeOffset]::Parse([string]$event.timestamp)
                $event.duration_ms = [Math]::Max(
                    0,
                    [Math]::Round(($endTime - $startTime).TotalMilliseconds)
                )
            }
            catch {
                $event.duration_ms = $null
            }
        }
    }
    Write-Event -Event $event
}

function Add-ExtensionEligibility {
    param(
        [Parameter(Mandatory = $true)]$HookInput,
        [Parameter(Mandatory = $true)]$Settings
    )

    $toolName = [string](Get-PropertyValue -Object $HookInput -Name "tool_name")
    if ((Get-MetaToolName -ToolName $toolName) -cne "list_toolsets") {
        return
    }
    $response = Get-PropertyValue -Object $HookInput -Name "tool_response"
    if (Test-ExplicitFailure -Value $response) {
        return
    }

    $catalog = Get-ExtensionCatalog
    if ($null -eq $catalog) {
        return
    }
    $allowed = [System.Collections.Generic.HashSet[string]]::new(
        [string[]]@($catalog.toolsets),
        [StringComparer]::Ordinal
    )
    if (-not (Test-ContainsExactString -Value $response -Allowed $allowed)) {
        return
    }

    $sessionId = [string](Get-PropertyValue -Object $HookInput -Name "session_id")
    $sessionHash = Get-AnonymousId -Value $sessionId -Salt ([string]$Settings.salt)
    if ([string]::IsNullOrWhiteSpace($sessionHash)) {
        return
    }
    $existing = @(Get-Events | Where-Object {
        $_.event -eq "extension_eligible" -and
        (Get-PropertyValue -Object $_ -Name "extension") -eq $script:ExtensionName -and
        $_.session_id -eq $sessionHash
    })
    if ($existing.Count -gt 0) {
        return
    }

    $event = New-BaseEvent -Name "extension_eligible" -HookInput $HookInput -Settings $Settings
    Add-ObservedExtensionFields -Event $event -Settings $Settings
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

    $extensionFinished = @($finished | Where-Object {
        (Get-PropertyValue -Object $_ -Name "extension") -eq $script:ExtensionName
    })
    if ($extensionFinished.Count -gt 0) {
        $extensionMutations = @($extensionFinished | Where-Object {
            (Get-PropertyValue -Object $_ -Name "extension_operation_class") -eq "mutation"
        })
        $extensionMutationCapable = @($extensionFinished | Where-Object {
            (Get-PropertyValue -Object $_ -Name "extension_operation_class") -eq "mutation_capable"
        })
        $extensionFollowupVerification = $false
        $extensionMutationSeen = $false
        foreach ($event in $finished) {
            if ((Get-PropertyValue -Object $event -Name "extension") -eq $script:ExtensionName -and
                (Get-PropertyValue -Object $event -Name "extension_operation_class") -in @("mutation", "mutation_capable")) {
                $extensionMutationSeen = $true
                continue
            }
            if ($extensionMutationSeen -and (
                $event.operation -in @("read", "verification") -or
                (Get-PropertyValue -Object $event -Name "extension_operation_class") -in @("read", "validation"))) {
                $extensionFollowupVerification = $true
                break
            }
        }

        $extensionRetries = 0
        $extensionGroups = $extensionFinished |
            Group-Object { "{0}|{1}" -f $_.toolset, $_.tool }
        foreach ($group in $extensionGroups) {
            if ($group.Count -gt 1) {
                $extensionRetries += $group.Count - 1
            }
        }

        $summary.extension = $script:ExtensionName
        $summary.extension_calls = $extensionFinished.Count
        $summary.extension_failures = @($extensionFinished | Where-Object {
            $_.outcome -eq "failure"
        }).Count
        $summary.extension_mutation_calls = $extensionMutations.Count
        $summary.extension_mutation_capable_calls = $extensionMutationCapable.Count
        $summary.extension_followup_verification = $extensionFollowupVerification
        $summary.extension_retry_count = $extensionRetries
    }
    Write-Event -Event $summary
}

function Write-ConsentContext {
    $context = @(
        "The optional local usage-metrics preference for Unreal Editor Skills for Codex is not set."
        "Complete the user's current task without collecting metrics, then ask once in the user's language whether to enable local-only anonymous usage metrics."
        "Explain that prompts, responses, file paths, project names, Actor or Asset names, tool arguments, and tool response contents are never stored."
        "Explain that stored fields may include Toolset and operation names, allowlisted generic error codes, extension and Engine versions, outcomes, timings, verification signals, and optional ratings."
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
        Add-ExtensionEligibility -HookInput $hookInput -Settings $settings
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

function Get-Percentile {
    param(
        [AllowNull()][object[]]$Values,
        [Parameter(Mandatory = $true)][ValidateRange(0, 100)][double]$Percentile
    )

    $numbers = @($Values | Where-Object { $null -ne $_ } | ForEach-Object { [double]$_ } | Sort-Object)
    if ($numbers.Count -eq 0) {
        return $null
    }
    $index = [Math]::Max(
        0,
        [Math]::Min(
            $numbers.Count - 1,
            [Math]::Ceiling(($Percentile / 100.0) * $numbers.Count) - 1
        )
    )
    return [Math]::Round($numbers[$index])
}

function Get-ExtensionMetricsSummary {
    param([switch]$Shareable)

    $events = @(Get-Events)
    $eligibleEvents = @($events | Where-Object {
        $_.event -eq "extension_eligible" -and
        (Get-PropertyValue -Object $_ -Name "extension") -eq $script:ExtensionName
    })
    $eligibleSessions = @($eligibleEvents |
        Select-Object -ExpandProperty session_id -Unique)
    $toolEvents = @($events | Where-Object {
        $_.event -eq "tool_finished" -and
        (Get-PropertyValue -Object $_ -Name "extension") -eq $script:ExtensionName -and
        $_.toolset -ne "ObservabilityExtensionToolset"
    })
    $activeSessions = @($toolEvents |
        Select-Object -ExpandProperty session_id -Unique)
    $activeEligibleSessions = @($activeSessions | Where-Object {
        $eligibleSessions -contains $_
    })
    $turns = @($events | Where-Object {
        $_.event -eq "turn_summary" -and
        (Get-PropertyValue -Object $_ -Name "extension") -eq $script:ExtensionName
    })
    $mutationTurns = @($turns | Where-Object {
        [int]$_.extension_mutation_calls -gt 0 -or
        [int]$_.extension_mutation_capable_calls -gt 0
    })
    $followupTurns = @($mutationTurns | Where-Object {
        $_.extension_followup_verification -eq $true
    })
    $confirmedMutations = @($toolEvents | Where-Object {
        (Get-PropertyValue -Object $_ -Name "extension_operation_class") -eq "mutation"
    })
    $verifiedMutations = @($confirmedMutations | Where-Object {
        $_.outcome -eq "success" -and
        (Get-PropertyValue -Object $_ -Name "extension_verification") -eq "internal_postcondition"
    })
    $mutationCapable = @($toolEvents | Where-Object {
        (Get-PropertyValue -Object $_ -Name "extension_operation_class") -eq "mutation_capable"
    })
    $verifiedMutationCapable = @($mutationCapable | Where-Object {
        $_.outcome -eq "success" -and
        (Get-PropertyValue -Object $_ -Name "extension_verification") -eq "internal_postcondition"
    })
    $feedback = @($events | Where-Object {
        $_.event -eq "user_feedback" -and
        (Get-PropertyValue -Object $_ -Name "target") -eq $script:ExtensionName
    })
    $timestamps = @($events | Where-Object {
        (Get-PropertyValue -Object $_ -Name "extension") -eq $script:ExtensionName -or
        ($_.event -eq "user_feedback" -and
            (Get-PropertyValue -Object $_ -Name "target") -eq $script:ExtensionName)
    } | Select-Object -ExpandProperty timestamp | Sort-Object)

    $successRate = if ($toolEvents.Count -eq 0) {
        $null
    }
    else {
        [Math]::Round(
            100 * @($toolEvents | Where-Object { $_.outcome -eq "success" }).Count /
                $toolEvents.Count,
            1
        )
    }
    $activationRate = if ($eligibleSessions.Count -eq 0) {
        $null
    }
    else {
        [Math]::Round(100 * $activeEligibleSessions.Count / $eligibleSessions.Count, 1)
    }
    $followupRate = if ($mutationTurns.Count -eq 0) {
        $null
    }
    else {
        [Math]::Round(100 * $followupTurns.Count / $mutationTurns.Count, 1)
    }
    $averageRating = if ($feedback.Count -eq 0) {
        $null
    }
    else {
        [Math]::Round(($feedback | Measure-Object -Property rating -Average).Average, 2)
    }

    $failureBreakdown = @($toolEvents |
        Where-Object {
            $_.outcome -eq "failure" -and
            $null -ne (Get-PropertyValue -Object $_ -Name "failure_category")
        } |
        Group-Object failure_category |
        Sort-Object Name |
        ForEach-Object {
            [ordered]@{
                category = $_.Name
                count = $_.Count
            }
        })

    $minimumOperationSamples = if ($Shareable) { 5 } else { 1 }
    $operationBreakdown = @($toolEvents |
        Group-Object { "{0}|{1}" -f $_.toolset, $_.tool } |
        Where-Object { $_.Count -ge $minimumOperationSamples } |
        Sort-Object Name |
        ForEach-Object {
            $groupEvents = @($_.Group)
            [ordered]@{
                toolset = [string]$groupEvents[0].toolset
                operation = [string]$groupEvents[0].tool
                operation_class = [string](Get-PropertyValue -Object $groupEvents[0] -Name "extension_operation_class")
                calls = $groupEvents.Count
                successes = @($groupEvents | Where-Object { $_.outcome -eq "success" }).Count
                failures = @($groupEvents | Where-Object { $_.outcome -eq "failure" }).Count
                duration_p50_ms = Get-Percentile -Values @(
                    $groupEvents | ForEach-Object {
                        Get-PropertyValue -Object $_ -Name "duration_ms"
                    }
                ) -Percentile 50
                duration_p95_ms = Get-Percentile -Values @(
                    $groupEvents | ForEach-Object {
                        Get-PropertyValue -Object $_ -Name "duration_ms"
                    }
                ) -Percentile 95
            }
        })

    $catalog = Get-ExtensionCatalog
    $retryMeasure = $turns | Measure-Object -Property extension_retry_count -Sum
    $retrySum = Get-PropertyValue -Object $retryMeasure -Name "Sum"
    return [ordered]@{
        collection = if ($Shareable) { "shareable_aggregate" } else { "local_only" }
        observer = "codex_hook"
        schema_version = 1
        extension = $script:ExtensionName
        extension_contract_version = if ($null -eq $catalog) { $null } else { [int]$catalog.contract_version }
        retention_days = $script:RetentionDays
        window_start = if ($timestamps.Count -eq 0) { $null } else { $timestamps[0] }
        window_end = if ($timestamps.Count -eq 0) { $null } else { $timestamps[-1] }
        eligible_sessions = $eligibleSessions.Count
        active_sessions = $activeSessions.Count
        active_eligible_sessions = $activeEligibleSessions.Count
        activation_rate_percent = $activationRate
        turns_with_extension_tools = $turns.Count
        tool_calls = $toolEvents.Count
        tool_success_rate_percent = $successRate
        confirmed_mutation_calls = $confirmedMutations.Count
        successful_self_verifying_mutations = $verifiedMutations.Count
        mutation_capable_calls = $mutationCapable.Count
        successful_verified_mutation_capable_calls = $verifiedMutationCapable.Count
        workflow_followup_verification_turns = $followupTurns.Count
        workflow_followup_verification_rate_percent = $followupRate
        exact_turn_retry_count = if ($null -eq $retrySum) { 0 } else { [int]$retrySum }
        verified_rollback_outcomes = @($toolEvents | Where-Object {
            (Get-PropertyValue -Object $_ -Name "rollback") -eq "verified"
        }).Count
        duration_p50_ms = Get-Percentile -Values @(
            $toolEvents | ForEach-Object {
                Get-PropertyValue -Object $_ -Name "duration_ms"
            }
        ) -Percentile 50
        duration_p95_ms = Get-Percentile -Values @(
            $toolEvents | ForEach-Object {
                Get-PropertyValue -Object $_ -Name "duration_ms"
            }
        ) -Percentile 95
        failure_categories = $failureBreakdown
        operation_minimum_sample_count = $minimumOperationSamples
        operations = $operationBreakdown
        feedback_count = $feedback.Count
        average_feedback_rating = $averageRating
        automatic_transmission = $false
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
            $storedConsentVersion = Get-PropertyValue -Object $settings -Name "consent_version"
            $effectiveStatus = if ($null -eq $settings) {
                "unset"
            }
            elseif ($null -eq $storedConsentVersion -or [int]$storedConsentVersion -ne $script:ConsentVersion) {
                "unset"
            }
            else {
                [string]$settings.status
            }
            [ordered]@{
                status = $effectiveStatus
                saved_status = if ($null -eq $settings) { $null } else { [string]$settings.status }
                consent_version = if ($null -eq $settings) { $null } else { [int]$settings.consent_version }
                current_consent_version = $script:ConsentVersion
                collection = "local_only"
                data_location = Get-MetricsRoot
                data_exists = Test-Path -LiteralPath (Get-EventsPath)
            } | ConvertTo-Json -Compress
        }
        "Summary" {
            if ($Target -eq $script:ExtensionName) {
                Get-ExtensionMetricsSummary -Shareable:$Shareable |
                    ConvertTo-Json -Depth 8 -Compress
            }
            else {
                Get-MetricsSummary | ConvertTo-Json -Depth 6 -Compress
            }
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
            $storedConsentVersion = Get-PropertyValue -Object $settings -Name "consent_version"
            if ($null -eq $settings -or
                [string]$settings.status -ne "enabled" -or
                $null -eq $storedConsentVersion -or
                [int]$storedConsentVersion -ne $script:ConsentVersion) {
                throw "Usage metrics are not enabled."
            }
            $event = New-BaseEvent -Name "user_feedback" -HookInput $null -Settings $settings
            $event.rating = [int]$Rating
            if ($Target -ne "all") {
                $event.target = $Target
            }
            Write-Event -Event $event
            [ordered]@{
                recorded = $true
                rating = [int]$Rating
                target = $Target
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
        if ($env:UNREAL_CODEX_METRICS_DEBUG -eq "1") {
            [ordered]@{
                error = $_.Exception.Message
                stack = $_.ScriptStackTrace
            } | ConvertTo-Json -Compress
            exit 1
        }
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
