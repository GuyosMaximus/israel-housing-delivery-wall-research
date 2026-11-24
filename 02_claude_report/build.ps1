# build.ps1 — 4-pass build of the prep report (run from build/)
#   lualatex -> biber -> lualatex -> lualatex   (brief §4)
$ErrorActionPreference = 'Continue'
Set-Location -Path $PSScriptRoot
lualatex -interaction=nonstopmode main.tex | Out-Null
biber main
lualatex -interaction=nonstopmode main.tex | Out-Null
lualatex -interaction=nonstopmode main.tex | Out-Null
Write-Host '--- build summary ---'
Select-String -Path main.log -Pattern '^!', 'Output written', 'undefined', 'Overfull' | ForEach-Object { $_.Line }
