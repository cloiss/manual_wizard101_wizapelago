SHELL := powershell.exe
.SHELLFLAGS := -NoProfile -ExecutionPolicy Bypass -Command
ARCHIPELAGO_PATH = D:\ProgramData\Archipelago

package:
	Compress-Archive -Path "manual_wizard101_cloiss" -DestinationPath "manual_wizard101_cloiss.apworld" -Force

install:
	./manual_wizard101_cloiss.apworld
clean:
	if (Test-Path "manual_wizard101_cloiss.apworld") { Remove-Item -Path "manual_wizard101_cloiss.apworld" -Force }

generate:
	$(ARCHIPELAGO_PATH)\ArchipelagoGenerate.exe

host:
	$(ARCHIPELAGO_PATH)\ArchipelagoServer.exe

client:
	$(ARCHIPELAGO_PATH)\ArchipelagoLauncherDebug.exe "Manual Client"

.PHONY: package clean