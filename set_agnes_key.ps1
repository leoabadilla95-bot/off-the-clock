# Saves your free Agnes AI API key to your Windows user environment. The key is hidden as you paste it.
$s = Read-Host "Paste your Agnes AI API key, then press Enter" -AsSecureString
$k = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($s))
if ($k.Trim().Length -lt 10) { Write-Host "That looks too short. Run this again." ; return }
[Environment]::SetEnvironmentVariable("AGNES_API_KEY", $k.Trim(), "User")
Write-Host "Saved. Go back to Claude and say saved."
