# Export every slide of the deck to PNG with PowerPoint (for visual review).
$deck = Join-Path $PSScriptRoot "AI_Sentiment_Analyzer.pptx"
$out = Join-Path $env:TEMP "deck_render"
if (Test-Path $out) { Remove-Item $out -Recurse -Force }
New-Item -ItemType Directory -Force $out | Out-Null
$pp = New-Object -ComObject PowerPoint.Application
$pres = $pp.Presentations.Open($deck, $true, $false, $false)
$i = 1
foreach ($slide in $pres.Slides) {
    $slide.Export((Join-Path $out ("s{0:D2}.png" -f $i)), "PNG", 1280, 720)
    $i++
}
$pres.Close()
$pp.Quit()
Write-Output $out
