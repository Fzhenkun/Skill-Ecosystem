param()

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$collector = Join-Path $repoRoot "collect.ps1"
$tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("skill-tracker-copilot-session-state-" + [guid]::NewGuid().ToString("N"))
$fakeHome = Join-Path $tempRoot "home"
$skillDir = Join-Path $fakeHome ".copilot\skills\copilot-invoked-skill"
$sessionDir = Join-Path $fakeHome ".copilot\session-state\11111111-2222-3333-4444-555555555555"
$outputDir = Join-Path $tempRoot "dashboard"
$configPath = Join-Path $tempRoot "config.json"

try {
    New-Item -ItemType Directory -Path $skillDir,$sessionDir,$outputDir -Force | Out-Null
    $skillFile = Join-Path $skillDir "SKILL.md"
    [System.IO.File]::WriteAllText(
        $skillFile,
        "---`nname: copilot-invoked-skill`ndescription: Copilot skill.invoked fixture.`n---`n",
        [System.Text.Encoding]::UTF8
    )

    $event = [ordered]@{
        type = "skill.invoked"
        data = [ordered]@{
            name = "copilot-invoked-skill"
            path = $skillFile
            content = ("# Copilot invoked fixture`n" + [System.String]::new([char]'x', 150000))
            source = "personal-copilot"
            trigger = "agent-invoked"
        }
        id = "copilot-skill-event-1"
        timestamp = "2026-08-06T04:05:06Z"
    }
    $eventsPath = Join-Path $sessionDir "events.jsonl"
    [System.IO.File]::WriteAllText(
        $eventsPath,
        ($event | ConvertTo-Json -Depth 8 -Compress) + "`n",
        [System.Text.Encoding]::UTF8
    )
    if ((Get-Item -LiteralPath $eventsPath).Length -le 131072) {
        throw "Copilot skill.invoked fixture did not exceed the chunked-line threshold."
    }

    $config = [ordered]@{
        skills_root = ""
        skills_roots = @()
        output_dir = $outputDir
        max_log_entries = 100
        dedup_window_minutes = 2
        custom_tools = @()
    }
    [System.IO.File]::WriteAllText($configPath, ($config | ConvertTo-Json -Depth 6), [System.Text.Encoding]::UTF8)

    $priorUserProfile = $env:USERPROFILE
    $priorHome = $env:HOME
    $priorAppData = $env:APPDATA
    $priorLocalAppData = $env:LOCALAPPDATA
    $priorPath = $env:PATH
    try {
        $env:USERPROFILE = $fakeHome
        $env:HOME = $fakeHome
        $env:APPDATA = Join-Path $fakeHome "AppData\Roaming"
        $env:LOCALAPPDATA = Join-Path $fakeHome "AppData\Local"
        $env:PATH = "$env:SystemRoot\System32;$env:SystemRoot\System32\WindowsPowerShell\v1.0"
        & powershell -NoProfile -ExecutionPolicy Bypass -File $collector -ConfigFile $configPath -RecentFiles 0 -RecentDays 0 | Out-Null
        if ($LASTEXITCODE -ne 0) { throw "Collector failed." }
    } finally {
        $env:USERPROFILE = $priorUserProfile
        $env:HOME = $priorHome
        $env:APPDATA = $priorAppData
        $env:LOCALAPPDATA = $priorLocalAppData
        $env:PATH = $priorPath
    }

    $toolReport = Get-Content -LiteralPath (Join-Path $outputDir "tool_report.json") -Raw -Encoding UTF8 | ConvertFrom-Json
    $installedTools = @($toolReport.summary.installed_tools | ForEach-Object { [string]$_ })
    if ($installedTools -notcontains "GitHub Copilot") {
        throw "GitHub Copilot was not detected from .copilot/session-state."
    }
    $copilotRows = @($toolReport.sources | Where-Object { $_.tool -eq "GitHub Copilot" -and $_.detected })
    if ($copilotRows.Count -eq 0) {
        throw "GitHub Copilot detected source row is missing."
    }

    $catalog = Get-Content -LiteralPath (Join-Path $outputDir "skill_catalog.json") -Raw -Encoding UTF8 | ConvertFrom-Json
    if (-not @($catalog | Where-Object skill -eq "copilot-invoked-skill")) {
        throw "Copilot skill.invoked did not discover the skill in the catalog."
    }
    $log = Get-Content -LiteralPath (Join-Path $outputDir "skill_log.js") -Raw -Encoding UTF8
    if ($log -notmatch '"tool":"GitHub Copilot"' -or
        $log -notmatch '"skill":"copilot-invoked-skill"' -or
        $log -notmatch '"time":"2026-08-06T04:05:06Z"') {
        throw "Copilot skill.invoked did not produce the expected dated skill log row."
    }

    Write-Host "Collector Copilot session-state test passed."
} finally {
    if (Test-Path -LiteralPath $tempRoot) {
        Remove-Item -LiteralPath $tempRoot -Recurse -Force
    }
}
