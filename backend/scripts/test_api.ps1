$BaseUrl = "http://127.0.0.1:8000"

Write-Host ""
Write-Host "=== GET /health ==="
Invoke-RestMethod "$BaseUrl/health" | ConvertTo-Json -Depth 5

Write-Host ""
Write-Host "=== GET /characters ==="
Invoke-RestMethod "$BaseUrl/characters" | ConvertTo-Json -Depth 5

Write-Host ""
Write-Host "=== POST /advice ==="

$body = @{
    character = @{
        character_id     = "gentle_mina"
        display_name     = "ミナ"
        personality_type = "gentle"
        speaking_style   = "casual"
        advice_style     = "rest_focused"
    }
    sleep = @{
        date                = "2026-04-28"
        total_sleep_minutes = 372
        efficiency          = 86
        deep_sleep_minutes  = 52
        rem_sleep_minutes   = 78
        awake_minutes       = 31
    }
    mood = "tired"
} | ConvertTo-Json -Depth 5

Invoke-RestMethod `
    -Uri "$BaseUrl/advice" `
    -Method Post `
    -ContentType "application/json; charset=utf-8" `
    -Body $body |
    ConvertTo-Json -Depth 5