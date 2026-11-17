# Saves your Runway API key to your Windows user environment. The key is hidden as you paste it.
$s = Read-Host "Paste your Runway API key, then press Enter" -AsSecureString
$k = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($s))
if ($k.Trim().Length -lt 20) { Write-Host "That looks too short. Run this again." ; return }
[Environment]::SetEnvironmentVariable("RUNWAYML_API_SECRET", $k.Trim(), "User")
Write-Host "Saved. Go back to Claude and say saved."
