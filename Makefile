SHELL := powershell.exe
.SHELLFLAGS := -NoProfile -ExecutionPolicy Bypass -Command

package:
	Compress-Archive -Path "manual_wizard101_cloiss" -DestinationPath "manual_wizard101_cloiss.apworld" -Force

clean:
	if (Test-Path "manual_wizard101_cloiss.apworld") { Remove-Item -Path "manual_wizard101_cloiss.apworld" -Force }

.PHONY: package clean