# Cloud Training Guide (Civitai)

Da dein PC für das Training zu wenig RAM hat, nutzen wir Civitai. Das ist einfach, schnell und liefert professionelle Ergebnisse.

## 1. Vorbereitung
Ich habe dir bereits alle Bilder in eine ZIP-Datei gepackt:
👉 `C:\Users\k4_PC\Projekte\ai_influencer\training_data\lena_dataset.zip`

## 2. Training starten
1.  Geh auf [civitai.com/generate](https://civitai.com/generate) (Logge dich ein).
2.  Klicke oben rechts auf **"Train a LoRA"**.
3.  **Model Selection**:
    *   Base Model: **Flux.1 Dev** (Wichtig!)
4.  **Concept**:
    *   Name: `lena_marie_v1`
    *   Trigger Word: `lena_marie`
5.  **Dataset**:
    *   Upload die Datei `lena_dataset.zip`.
6.  **Training Parameters (Wichtig!)**:
    *   **Preset**: Wähle "Standard" oder "Rapid" (Standard ist besser).
    *   **Epochs**: Erhöhe das auf **15** oder **20**. (5 ist zu wenig für 30 Bilder).
    *   **Repeats**: Klicke ggf. auf dein Dataset (oder das Zahnrad daneben). Stelle Repeats auf **5** oder **10**.
    *   **Ziel**: Du willst rechts in der Zusammenfassung ca. **2000 bis 2500 "Total Steps"** sehen.
        *   *Rechnung:* 30 Bilder × 10 Repeats × 7 Epochs ≈ 2100 Steps.
        *   *Verstell Epochs so lange, bis du bei ~2000-2500 landest.*
    *   **Resolution**: Stelle das auf **1024**. (512 ist für Flux zu wenig!).
    *   **Batch Size**: 1.
    *   **Optimizer**: AdamW8bit (Default lassen).
7.  **Kosten**: Das kostet ca. 500 "Buzz" (ca. 0,50$). Man bekommt oft Buzz geschenkt für das Bewerten von Bildern, oder man kauft für 5$ ein Paket.

## 3. Nach dem Training
1.  Du bekommst eine E-Mail, wenn es fertig ist (ca. 15-30 Min).
2.  Lade die Datei (`lena_marie_v1.safetensors`) herunter.
3.  Verschiebe sie in deinen ComfyUI Ordner:
    `C:\Users\k4_PC\Projekte\ai_influencer\ComfyUI\models\loras\`

Danach können wir die LoRA in ComfyUI testen! 🚀
