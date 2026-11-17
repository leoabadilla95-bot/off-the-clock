# Saves your ElevenLabs API key to your Windows user environment. The key is hidden as you paste it.
$s = Read-Host "Paste your ElevenLabs API key, then press Enter" -AsSecureString
$k = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($s))
if ($k.Trim().Length -lt 20) { Write-Host "That looks too short. Run this again." ; return }
[Environment]::SetEnvironmentVariable("ELEVENLABS_API_KEY", $k.Trim(), "User")
Write-Host "Saved. Go back to Claude and say saved."
