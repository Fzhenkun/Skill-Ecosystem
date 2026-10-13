param()

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("skill-tracker-local-skills-sync-" + [guid]::NewGuid().ToString("N"))
$packageRoot = Join-Path (Join-Path $tempRoot "tools") "skill-tracker"
$repoSkillsRoot = Join-Path $tempRoot "skills"
$repoSkillDir = Join-Path $repoSkillsRoot "local-sync-skill"
$fakeHome = Join-Path $tempRoot "home"
$logDir = Join-Path $tempRoot "logs"
$port = Get-Random -Minimum 34000 -Maximum 39000

function Copy-RequiredFile {
    param([string]$RelativePath)
    $source = Join-Path $repoRoot $RelativePath
    $destination = Join-Path $packageRoot $RelativePath
    New-Item -ItemType Directory -Path (Split-Path -Parent $destination) -Force | Out-Null
    Copy-Item -LiteralPath $source -Destination $destination -Force
}

try {
    New-Item -ItemType Directory -Path $repoSkillDir,$logDir -Force | Out-Null
    New-Item -ItemType Directory -Path (Join-Path $repoSkillDir "references") -Force | Out-Null
    [System.IO.File]::WriteAllText(
        (Join-Path $repoSkillDir "SKILL.md"),
        "---`nname: local-sync-skill`ndescription: Local sync fixture.`n---`n`nFresh repository version.`n",
        [System.Text.Encoding]::UTF8
    )
    [System.IO.File]::WriteAllText(
        (Join-Path $repoSkillDir "references\workflow.md"),
        "Nested asset copied from repository.`n",
        [System.Text.Encoding]::UTF8
    )
    [System.IO.File]::WriteAllText(
        (Join-Path $logDir "session.jsonl"),
        '{"type":"USER_INPUT","timestamp":"2026-08-07T04:00:00Z","text":"/local-sync-skill "}' + "`n",
        [System.Text.Encoding]::UTF8
    )

    foreach ($relativePath in @("collect.ps1", "start-dashboard.ps1", "dashboard/index.html", "dashboard/demo_data.js", "tools/platform-paths.psm1", "scripts/manage-shortcut.ps1")) {
        Copy-RequiredFile -RelativePath $relativePath
    }
    $config = [ordered]@{
        skills_root = ""
        skills_roots = @($repoSkillsRoot)
        output_dir = "./dashboard"
        max_log_entries = 100
        dedup_window_minutes = 2
        custom_tools = @([ordered]@{ name = "Local Sync Fixture"; path = $logDir })
    }
    [System.IO.File]::WriteAllText((Join-Path $packageRoot "config.json"), ($config | ConvertTo-Json -Depth 6), [System.Text.Encoding]::UTF8)

    $codexExisting = Join-Path $fakeHome ".codex\skills\local-sync-skill"
    New-Item -ItemType Directory -Path $codexExisting -Force | Out-Null
    [System.IO.File]::WriteAllText((Join-Path $codexExisting "old.txt"), "old local file`n", [System.Text.Encoding]::UTF8)
    [System.IO.File]::WriteAllText((Join-Path $codexExisting "SKILL.md"), "old local skill`n", [System.Text.Encoding]::UTF8)

    $priorUserProfile = $env:USERPROFILE
    $priorHome = $env:HOME
    $priorAppData = $env:APPDATA
    $priorLocalAppData = $env:LOCALAPPDATA
    try {
        $env:USERPROFILE = $fakeHome
        $env:HOME = $fakeHome
        $env:APPDATA = Join-Path $fakeHome "AppData\Roaming"
        $env:LOCALAPPDATA = Join-Path $fakeHome "AppData\Local"

        & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $packageRoot "start-dashboard.ps1") -Port $port -NoBrowser
        if ($LASTEXITCODE -ne 0) { throw "Launcher failed to start." }

        $response = Invoke-WebRequest -Uri "http://127.0.0.1:$port/api/local-skills/sync" -Method Post -UseBasicParsing -TimeoutSec 10
        if ($response.StatusCode -ne 200) { throw "Local skill sync returned HTTP $($response.StatusCode), expected 200." }
        $payload = $response.Content | ConvertFrom-Json
        if (-not $payload.success -or $payload.skill_count -ne 1 -or $payload.item_count -ne 3) {
            throw "Unexpected sync response: $($payload | ConvertTo-Json -Compress)"
        }

        foreach ($toolDir in @(".codex", ".copilot", ".claude")) {
            $target = Join-Path $fakeHome (Join-Path $toolDir "skills\local-sync-skill")
            $skillPath = Join-Path $target "SKILL.md"
            $nestedPath = Join-Path $target "references\workflow.md"
            if (-not (Test-Path -LiteralPath $skillPath -PathType Leaf)) {
                throw "$toolDir target did not receive SKILL.md."
            }
            if ((Get-Content -LiteralPath $skillPath -Raw -Encoding UTF8) -notmatch "Fresh repository version") {
                throw "$toolDir target was not replaced with the repository skill."
            }
            if (-not (Test-Path -LiteralPath $nestedPath -PathType Leaf)) {
                throw "$toolDir target did not receive nested skill assets."
            }
        }
        if (Test-Path -LiteralPath (Join-Path $codexExisting "old.txt")) {
            throw "Existing Codex skill directory was not replaced."
        }
    } finally {
        $env:USERPROFILE = $priorUserProfile
        $env:HOME = $priorHome
        $env:APPDATA = $priorAppData
        $env:LOCALAPPDATA = $priorLocalAppData
    }

    Write-Host "Local skills sync API test passed."
} finally {
    Get-CimInstance Win32_Process -Filter "Name = 'powershell.exe'" |
        Where-Object { $_.CommandLine -and $_.CommandLine.Contains($packageRoot) } |
        ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
    if (Test-Path -LiteralPath $tempRoot) {
        Remove-Item -LiteralPath $tempRoot -Recurse -Force
    }
}
