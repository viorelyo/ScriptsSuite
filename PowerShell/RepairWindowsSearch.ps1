$registryPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Search"

New-ItemProperty -Path $registryPath -Name "BingSearchEnabled" -Value 0 -PropertyType "DWord"
Set-ItemProperty -Path $registryPath -Name "CortanaConsent" -Value 0

taskkill /F /IM searchui.exe
taskkill /F /IM explorer.exe
explorer.exe