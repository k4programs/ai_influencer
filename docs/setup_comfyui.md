# ComfyUI Installation & AI Integration Guide

## 1. ComfyUI Installation (The Engine)
Wir installieren **ComfyUI Protable** (am einfachsten für Windows) und den **Manager**.

### Schritt-für-Schritt
1. **Download**:
   - Lade die "ComfyUI_windows_portable_nvidia_cu121_or_cpu.7z" von der [offiziellen GitHub Seite](https://github.com/comfyanonymous/ComfyUI/releases) herunter.
   - *Hinweis: Die Datei ist groß (~1.4GB).*
2. **Entpacken**:
   - Entpacke die Datei direkt nach: `C:\Users\k4_PC\Projekte\ai_influencer\ComfyUI`
   - *Wichtig: Keine Leerzeichen im Pfad!*
3. **Manager Installieren** (WICHTIG für mich):
   - Gehe in den Ordner: `ComfyUI\custom_nodes`
   - Öffne dort ein Terminal (`Rechtsklick` -> `Im Terminal öffnen` oder `Git Bash here`).
   - Führe aus: `git clone https://github.com/ltdrdata/ComfyUI-Manager.git`
4. **Starten**:
   - Gehe zurück in den Hauptordner `ComfyUI`.
   - Doppelklick auf `run_nvidia_gpu.bat`.
   - Der Browser sollte sich öffnen auf `http://127.0.0.1:8188`.

## 2. Wie ich (Die AI) das steuere?
Ich kann keine Maus bewegen, aber ich kann **Code** schreiben, der mit ComfyUI "spricht".

### Die Architektur
1. **Du (Host)**: Lässt ComfyUI im Hintergrund laufen (`run_nvidia_gpu.bat`).
2. **Die Schnittstelle (API)**: ComfyUI hört auf Port `8188`.
3. **Ich (Agent)**:
   - Ich erstelle **JSON-Workflows** (Baupläne für Bilder).
   - Ich schreibe **Python-Skripte**, die diese JSONs an `http://127.0.0.1:8188/prompt` senden.
   - Ich kann Ordner überwachen und prüfen, wann das Bild fertig ist.

### Was ich von dir brauche
Damit das klappt, müssen wir später sicherstellen, dass deine Firewall lokale Anfragen auf Port 8188 erlaubt (meistens Standard).

## 3. Nächste Schritte nach der Installation
Sobald ComfyUI läuft:
1. Wir installieren den **Flux.1 Checkpoint** (Das Gehirn für die Bilder).
2. Wir erstellen den ersten Workflow gemeinsam.
3. Deine Aufgabe: Einfach nur installieren und bestätigen, dass es läuft.
