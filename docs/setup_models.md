# Flux.1 Model Setup Guide

Perfekt, die Verbindung steht! 🚀
Jetzt brauchen wir das "Gehirn" der Bildgenerierung: **Flux.1 [dev]**.
Da du eine RTX 3080 Ti (12GB VRAM) hast, nutzen wir die **FP8 Version**, die ist fast genauso gut wie die volle Version, aber passt in deinen Speicher.

## 1. Download Dateien
Bitte lade diese 3 Dateien herunter und speichere sie in den exakten Ordnern.

### A. Das Haupt-Model (Checkpoint)
- **Datei**: `flux1-dev-fp8.safetensors`
- **Download Link**: [HuggingFace - Kijai Flux-FP8](https://huggingface.co/kijai/flux-fp8/resolve/main/flux1-dev-fp8.safetensors?download=true)
- **Speicherort**: `C:\Users\k4_PC\Projekte\ai_influencer\ComfyUI\models\checkpoints`

### B. Die Text-Encoder (CLIP)
Flux braucht zwei Text-Versteher, um deine Prompts zu lesen.
*Es kann sein, dass ComfyUI diese automatisch lädt, aber manuell ist sicherer.*

**Datei 1 (T5 Large):**
- **Datei**: `t5xxl_fp8_e4m3fn.safetensors`
- **Download Link**: [HuggingFace - ComfyOrg](https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp8_e4m3fn.safetensors?download=true)
- **Speicherort**: `C:\Users\k4_PC\Projekte\ai_influencer\ComfyUI\models\clip`

**Datei 2 (CLIP L):**
- **Datei**: `clip_l.safetensors`
- **Download Link**: [HuggingFace - ComfyOrg](https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors?download=true)
- **Speicherort**: `C:\Users\k4_PC\Projekte\ai_influencer\ComfyUI\models\clip`

### C. Der Decoder (VAE)
**Datei (VAE):**
- **Datei**: `ae.safetensors`
- **Download Link (Alternative)**: [HuggingFace - Camenduru (Mirror)](https://huggingface.co/camenduru/FLUX.1-dev/resolve/main/ae.safetensors?download=true)
- **Speicherort**: `C:\Users\k4_PC\Projekte\ai_influencer\ComfyUI\models\vae`

---

## 2. Check
Wenn du alles runtergeladen hast, drücke im ComfyUI Fenster auf **"Refresh"** (rechts im Menü).

## 3. Der Test
Ich erstelle dir gleich einen Workflow, den du laden kannst, um zu testen, ob alles klappt.
