# Intelligence Engine Setup (Ollama)

Wir nutzen **Ollama** als lokales "Gehirn" für Lena-Marie.
Es ermöglicht ihr, Texte zu schreiben, auf Kommentare zu antworten und eigene Bildideen zu entwickeln.

## 1. Installation & Status
- **Status:** Installiert (via winget)
- **Pfad:** `%LOCALAPPDATA%\Programs\Ollama\ollama.exe`
- **Model:** `llama3.2` (3B Parameter) - Schnell, effizient, smart.

## 2. Nutzung
Um mit Lena zu chatten (im Terminal):
```powershell
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" run llama3.2
```

## 3. System Prompt (Lena's Persönlichkeit)
Damit Llama 3.2 nicht als langweiliger Assistent antwortet, sondern als Lena, müssen wir ihm eine "Rolle" geben.
Das machen wir später via Modelfile oder API.

**Basis-Prompt:**
> "You are Lena-Marie, a 21-year-old DevOps engineer from Munich. You love hiking, tech, and cozy gaming sessions. You are sarcastic, smart, and use emojis. You speak German and English."

## 4. Integration (Zukunft)
Später verbinden wir Ollama mit:
1.  **Python-Skripten**: Um automatisch Captions für Instagram zu schreiben.
2.  **ComfyUI**: Um Prompts für den Flux-Generator zu variieren ("Creative Upscaling").
