param()

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$collector = Join-Path $repoRoot "collect.ps1"
$tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("skill-tracker-codex-read-" + [guid]::NewGuid().ToString("N"))
$fakeHome = Join-Path $tempRoot "home"
$seedRoot = Join-Path $fakeHome "seed-skills"
$externalSkillDir = Join-Path $fakeHome "external\skills\codex-latest-skill"
$selectedSkillDir = Join-Path $fakeHome ".codex\skills\.system\codex-selected-skill"
$codexLogDir = Join-Path $fakeHome ".codex\sessions\2026\08\05"
$outputDir = Join-Path $tempRoot "dashboard"
$configPath = Join-Path $tempRoot "config.json"

try {
    $collectorOutput = ""
    # Codex is considered active when the modern session root exists.
    New-Item -ItemType Directory -Path (Join-Path $seedRoot "seed-skill"),$externalSkillDir,$selectedSkillDir,$codexLogDir -Force | Out-Null
    [System.IO.File]::WriteAllText(
        (Join-Path $seedRoot "seed-skill\SKILL.md"),
        "---`nname: seed-skill`ndescription: Seed fixture.`n---`n",
        [System.Text.Encoding]::UTF8
    )
    $skillFile = Join-Path $externalSkillDir "SKILL.md"
    [System.IO.File]::WriteAllText(
        $skillFile,
        "---`nname: codex-latest-skill`ndescription: Read from a new Codex tool-call record.`n---`n",
        [System.Text.Encoding]::UTF8
    )
    $selectedSkillFile = Join-Path $selectedSkillDir "SKILL.md"
    [System.IO.File]::WriteAllText(
        $selectedSkillFile,
        "---`nname: codex-selected-skill`ndescription: Selected through Codex skill instructions.`n---`n",
        [System.Text.Encoding]::UTF8
    )
    $record = [ordered]@{
        timestamp = "2026-08-05T03:04:05Z"
        type = "response_item"
        payload = [ordered]@{
            type = "custom_tool_call"
            name = "Read"
            input = "Get-Content -Raw '$skillFile'"
        }
    }
    $selectedRecord = [ordered]@{
        timestamp = "2026-08-05T03:06:07Z"
        type = "response_item"
        payload = [ordered]@{
            type = "message"
            role = "user"
            content = @(
                [ordered]@{
                    type = "input_text"
                    text = "<skill>`n<name>codex-selected-skill</name>`n<path>$selectedSkillFile</path>`n---`nname: codex-selected-skill`ndescription: Selected fixture.`n---`n`n</skill>"
                }
            )
            internal_chat_message_metadata_passthrough = [ordered]@{
                content_item_kinds = @("skills.selected_skill_instructions")
            }
        }
    }
    $recordLine = ($record | ConvertTo-Json -Depth 8 -Compress)
    $selectedRecordLine = ($selectedRecord | ConvertTo-Json -Depth 8 -Compress)
    $codexLogPath = Join-Path $codexLogDir "session.jsonl"
    [System.IO.File]::WriteAllText(
        $codexLogPath,
        $recordLine + "`n" + $selectedRecordLine + "`n",
        [System.Text.Encoding]::UTF8
    )
    [System.IO.File]::AppendAllText(
        $codexLogPath,
        [System.String]::new([char]'x', 11000000),
        [System.Text.Encoding]::UTF8
    )
    if ((Get-Item -LiteralPath $codexLogPath).Length -le 10485760) {
        throw "Codex large-log fixture did not exceed 10 MiB."
    }
    $config = [ordered]@{
        skills_root = ""
        skills_roots = @($seedRoot)
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
    try {
        $env:USERPROFILE = $fakeHome
        $env:HOME = $fakeHome
        $env:APPDATA = Join-Path $fakeHome "AppData\Roaming"
        $env:LOCALAPPDATA = Join-Path $fakeHome "AppData\Local"
        $collectorOutput = (& powershell -NoProfile -ExecutionPolicy Bypass -File $collector -ConfigFile $configPath -RecentFiles 0 -RecentDays 0 2>&1 | Out-String)
        if ($LASTEXITCODE -ne 0) { throw "Collector failed." }
    } finally {
        $env:USERPROFILE = $priorUserProfile
        $env:HOME = $priorHome
        $env:APPDATA = $priorAppData
        $env:LOCALAPPDATA = $priorLocalAppData
    }

    $catalog = Get-Content -LiteralPath (Join-Path $outputDir "skill_catalog.json") -Raw -Encoding UTF8 | ConvertFrom-Json
    if (-not @($catalog | Where-Object skill -eq "codex-selected-skill")) {
        throw "Codex selected-skill instruction record did not discover the skill in the catalog."
    }
    $log = Get-Content -LiteralPath (Join-Path $outputDir "skill_log.js") -Raw -Encoding UTF8
    if ($log -notmatch '"skill":"codex-selected-skill"' -or $log -notmatch '"time":"2026-08-05T03:06:07Z"') {
        throw "Codex selected_skill_instructions did not produce the selected skill record."
    }

    Write-Host "Collector Codex latest-read test passed."
} finally {
    if (Test-Path -LiteralPath $tempRoot) {
        Remove-Item -LiteralPath $tempRoot -Recurse -Force
    }
}
