SHELL := powershell.exe
.SHELLFLAGS := -NoProfile -ExecutionPolicy Bypass -Command
ARCHIPELAGO_PATH = D:\ProgramData\Archipelago

package:
	Compress-Archive -Path "manual_wizard101_cloiss" -DestinationPath "manual_wizard101_cloiss.apworld" -Force

install:
	./manual_wizard101_cloiss.apworld
clean:
	if (Test-Path "manual_wizard101_cloiss.apworld") { Remove-Item -Path "manual_wizard101_cloiss.apworld" -Force }

package-automark:
	Copy-Item -Path "manual_wizard101_cloiss\data\locations.json" -Destination "automark_client\locations.json" -Force; Compress-Archive -Path "automark_client" -DestinationPath "automark_client.apworld" -Force; Remove-Item -Path "automark_client\locations.json" -Force

generate:
	$(ARCHIPELAGO_PATH)\ArchipelagoGenerate.exe
gen: generate

host:
	$(ARCHIPELAGO_PATH)\ArchipelagoServer.exe

client:
	$(ARCHIPELAGO_PATH)\ArchipelagoLauncherDebug.exe "Manual Client"

.PHONY: package clean package-automark