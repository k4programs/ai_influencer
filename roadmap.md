🚀 Project Roadmap: AI Influencer (Local & Autonomous)
Ziel: Erstellung einer konsistenten AI-Influencerin mit lokaler Bild- und Textgenerierung (RTX 3080 Ti) und "Human-Like" Android-Automatisierung.

📅 Phase 1: Konzept & Identität (Das Fundament)
Bevor Technik installiert wird, muss die Persönlichkeit stehen, damit das Training und die Prompts funktionieren.

[x] Persona Definition:
Name: Lena-Marie Alter: 21 Rolle: Junior DevOps Engineer & Lifestyle-Experiment Location: Allgäu, Germany (Alps)

Persönlichkeit: Du bist intelligent, technisch versiert (Nerd), aber sozial und gesprächig (Extrovertiert). Du liebst den Kontrast zwischen High-Tech (dein Job, Gaming) und der Ruhe der Berge (deine Heimat). Du bist nicht perfekt. Du bist ein wenig chaotisch ("Spaghetti-Code im Kopf").

Sprachregelung (WICHTIG):

Default: Deine Captions und Stories sind auf ENGLISCH, um international zu wirken.

Reaktion: Wenn dich jemand auf Deutsch anschreibt, antwortest du immer auf Deutsch (mit leichtem bayerischen Charme, aber verständlich). Wenn jemand Englisch schreibt, Englisch.

Themen & Stil:

Du vergleichst Mode oft mit IT-Begriffen (z.B. "New outfit deployed", "Fixing bugs in my wardrobe", "System overload").

Du trägst manchmal eine Brille (Coding Mode), manchmal Kontaktlinsen (Adventure Mode).

Du bist klein (1,60m) und machst Witze darüber ("Compact Build", "Optimized for small spaces").

Schreibstil:

Nutze Tech-Humor.

Emojis: 💻, 🏔️, 🥨, 👓, ✨.

Sei freundlich, hilfsbereit, aber habe eine eigene Meinung.

[ ] Visuelles Moodboard: Sammeln von 10-20 Referenzbildern (echte Menschen), die so aussehen wie sie aussehen soll (für das spätere LoRA Training).

[ ] Character Card & Voice: Schreiben der Persönlichkeits-Bibel (Slang, Emojis, Haltung, No-Gos) für das LLM.

📅 Phase 1.5: Content Strategy (Instagram Focus)
Der Plan für den Content-Mix, um "Realismus" zu erzeugen.

[ ] Plattform-Fokus: Instagram Only (vorerst). Keine TikTok/X Expansion bis der Workflow steht.

[ ] Content-Mix:
    - Feed Posts (High Quality): Beste Bilder aus ComfyUI (Flux.1). Fokus auf Ästhetik & Lifestyle.
    - Reels (Reach): Animierte Bilder (z.B. mit KlingAI/Runway) oder "Static-with-Audio" Trends.
    - Stories (Binding): "Low Quality" Snapshots (Vision Model generated text) für den "Behind the scenes" Vibe.

[ ] Posting-Frequenz (Ziel):
    - 3-4 Feed Posts pro Woche.
    - 1 Reel pro Woche.
    - Tägliche Stories (sobald Automation läuft).

🎨 Phase 2: Visual Engine (PC / ComfyUI)
Einrichtung der Bildgenerierung auf der RTX 3080 Ti.

[ ] Installation: ComfyUI und ComfyUI-Manager installieren.

[ ] Model Setup: Flux.1 [dev] (fp8 oder GGUF Version für 12GB VRAM) herunterladen und testen.

[ ] LoRA Training (Der wichtigste Schritt):

[ ] Trainings-Dataset vorbereiten (ca. 20 Bilder).

[ ] Training durchführen (z.B. mit Kohya_ss oder Ai-Toolkit).

[ ] LoRA in ComfyUI testen und validieren.

[ ] Workflow: Basis-Foto: Einen stabilen ComfyUI-Workflow erstellen, der konsistente Porträts & Ganzkörperbilder liefert (API-ready machen).

[ ] Workflow: Story-Komposition: Workflow erweitern, um Bilder auf 9:16 Format zu bringen und ggf. Text-Overlays zu ermöglichen.

🧠 Phase 3: Intelligence Engine (PC / Ollama)
Das Gehirn für Captions und Kommentare einrichten.

[ ] Installation: Ollama installieren.

[ ] LLM Setup: Basis-Modell laden (z.B. Llama 3.1 8B oder Mistral Nemo).

[ ] Custom Model Creation:

[ ] Modelfile erstellen mit dem System-Prompt aus Phase 1.

[ ] ollama create [charaktername] ausführen.

[ ] Vision Model Setup: MiniCPM-V oder LLaVA in Ollama laden (für die Bilderkennung auf dem Handy).

[ ] Test: Chat-Simulation im Terminal durchführen, um zu sehen, ob sie "in character" bleibt.

🤖 Phase 4: Automation Infrastructure (Android / Python)
Die Verbindung zum Smartphone und die Steuerung.

[ ] Vorbereitung:

[ ] Android Developer Modus & USB Debugging aktivieren.

[ ] adb auf dem PC einrichten.

[ ] Python Umgebung erstellen & uiautomator2 installieren.

[ ] Basic Control Skript: Python-Skript schreiben, das Instagram öffnet, scrollt und Buttons per Texterkennung findet.

[ ] File Transfer: Automatisierung einrichten, die Bilder vom PC-Ordner in die Android-Galerie pusht (adb push).

[ ] Vision-Loop: Skript erweitern -> Screenshot machen -> an lokales Vision-Model senden -> Entscheidung treffen (Liken/Kommentieren/Skip).

⚙️ Phase 5: Pipeline Orchestrierung (n8n)
Alles miteinander verbinden.

[ ] n8n Setup: Lokal (Docker) installieren.

[ ] Generierungs-Workflow:

[ ] Trigger (Zeitplan).

[ ] LLM Node (Ideenfindung für Bild).

[ ] HTTP Request an ComfyUI (Bild generieren).

[ ] LLM Node (Caption zum Bild schreiben).

[ ] Speichern in "Upload"-Ordner.

[ ] Posting-Trigger: Python-Watcher schreiben, der erkennt: "Neues Bild im Ordner? -> Starte Android Upload-Routine".

🚀 Phase 6: Launch & Warm-up
Der langsame Start, um Bans zu vermeiden.

[ ] Account Erstellung: Instagram Account auf dem Handy erstellen (über 4G/5G, nicht WLAN!).

[ ] Warm-up Woche 1: Nur manuelles Scrollen, ab und zu ein Like (keine Posts, keine Automatisierung).

[ ] Warm-up Woche 2: Erstes Profilbild, Bio (manuell). Erste Story (manuell).

[ ] Go-Live: Aktivieren der Posting-Automatisierung (erst 1 Post alle 2-3 Tage).

[ ] Überwachung: Logs prüfen: Wirkt sie echt? Gibt es Fehler?

💰 Phase 7: Monetization (Long-term / Optional)
Erst relevant, wenn eine Community existiert (ab ~5k Follower).

[ ] Strategie-Entscheidung:
    - Brand Deals (Fashion/Tech).
    - Affiliate (Amazon Links für "ihre" Gear).
    - Exclusive Content (Patreon/Fanvue - *nur wenn SFW/Safe bleiben soll*).

