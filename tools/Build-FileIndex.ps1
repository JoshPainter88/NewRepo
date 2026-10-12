<#
.SYNOPSIS
  Index a work folder so Cable Desk can find and open any file instantly.

.DESCRIPTION
  Scans the folder (recursively) and writes cabledesk-files.js next to cable-desk.html.
  The page picks it up on the next open: a Files view, project Files tabs, and file hits in search.
  Only names, folders, dates and sizes are recorded. File contents are never read, and nothing leaves your PC.
  Works with Windows PowerShell 5.1 and PowerShell 7.

.EXAMPLE
  powershell -NoProfile -ExecutionPolicy Bypass -File .\Build-FileIndex.ps1

.EXAMPLE
  powershell -NoProfile -ExecutionPolicy Bypass -File .\Build-FileIndex.ps1 -Root "D:\Jobs" -OutDir "C:\Work\CableDesk"
#>
[CmdletBinding()]
param(
  # Folder to index.
  [string]$Root = 'C:\Work',
  # Where cable-desk.html lives. Default: this script's folder, or ..\dist when run from the repo.
  [string]$OutDir = '',
  # Safety cap so a huge share cannot freeze the page.
  [int]$MaxFiles = 25000
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $Root -PathType Container)) {
  Write-Host "Folder not found: $Root" -ForegroundColor Red
  Write-Host 'Pass the right folder with -Root "C:\path\to\folder".'
  exit 1
}
$rootFull = (Resolve-Path -LiteralPath $Root).ProviderPath.TrimEnd('\', '/')

if (-not $OutDir) {
  $here = $PSScriptRoot
  $repoDist = Join-Path (Split-Path -Parent $here) 'dist'
  if (Get-ChildItem -LiteralPath $here -Filter 'cable-desk*.html' -ErrorAction SilentlyContinue) { $OutDir = $here }
  elseif (Test-Path -LiteralPath $repoDist -PathType Container) { $OutDir = $repoDist }
  else { $OutDir = $here }
}
if (-not (Test-Path -LiteralPath $OutDir -PathType Container)) { New-Item -ItemType Directory -Path $OutDir | Out-Null }

# Noise that never helps: build output, caches, Office lock files, OS litter.
$skipDirs = @('node_modules', '.git', '__pycache__', '.venv', '.vercel', '.tanstack', '.grok', '$RECYCLE.BIN', 'System Volume Information')
$skipFiles = @('Thumbs.db', 'desktop.ini', '.DS_Store')

function Test-Skip([string]$relative, [string]$name) {
  if ($name.StartsWith('~$')) { return $true }
  if ($skipFiles -contains $name) { return $true }
  foreach ($part in ($relative -split '[\\/]')) {
    if ($skipDirs -contains $part) { return $true }
  }
  return $false
}

function ConvertTo-JsonString([string]$s) {
  $sb = New-Object System.Text.StringBuilder ($s.Length + 8)
  [void]$sb.Append('"')
  foreach ($ch in $s.ToCharArray()) {
    $code = [int]$ch
    switch ($ch) {
      '"' { [void]$sb.Append('\"'); continue }
      '\' { [void]$sb.Append('\\'); continue }
      '<' { [void]$sb.Append('\u003c'); continue }
      default {
        if ($code -lt 0x20 -or $code -eq 0x2028 -or $code -eq 0x2029) { [void]$sb.AppendFormat('\u{0:x4}', $code) }
        else { [void]$sb.Append($ch) }
      }
    }
  }
  [void]$sb.Append('"')
  return $sb.ToString()
}

Write-Host "Indexing $rootFull ..."
$sw = [System.Diagnostics.Stopwatch]::StartNew()
$rows = New-Object System.Collections.Generic.List[string]
$skipped = 0
$truncated = $false

foreach ($f in (Get-ChildItem -LiteralPath $rootFull -Recurse -File -Force -ErrorAction SilentlyContinue)) {
  $rel = $f.FullName.Substring($rootFull.Length).TrimStart('\', '/')
  if (Test-Skip $rel $f.Name) { $skipped++; continue }
  if ($rows.Count -ge $MaxFiles) { $truncated = $true; break }
  $rel = $rel -replace '/', '\'
  $m = $f.LastWriteTime.ToString('yyyy-MM-dd HH:mm')
  $rows.Add('{"p":' + (ConvertTo-JsonString $rel) + ',"m":"' + $m + '","s":' + $f.Length + '}')
}

$stamp = (Get-Date).ToString('yyyy-MM-dd HH:mm')
$json = '{"root":' + (ConvertTo-JsonString $rootFull) + ',"indexed_at":"' + $stamp + '","count":' + $rows.Count +
        ',"truncated":' + $truncated.ToString().ToLower() + ',"files":[' + ($rows -join ',') + ']}'
$out = Join-Path $OutDir 'cabledesk-files.js'
[System.IO.File]::WriteAllText($out, "window.OS_FILES = $json;`n", (New-Object System.Text.UTF8Encoding $false))

$sw.Stop()
Write-Host ("Indexed {0:N0} files in {1:N1}s ({2:N0} skipped as noise)." -f $rows.Count, $sw.Elapsed.TotalSeconds, $skipped) -ForegroundColor Green
if ($truncated) { Write-Host "Stopped at $MaxFiles files. Raise -MaxFiles or point -Root at a narrower folder." -ForegroundColor Yellow }
Write-Host "Wrote $out"
