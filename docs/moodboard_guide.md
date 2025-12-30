# Visual Moodboard & Synthetic Data Guide

## Entscheidung: Synthetische Daten
Du möchtest die Trainingsbilder per AI generieren. Das ist eine **sehr gute Strategie**, um volle Kontrolle über das Aussehen zu haben.
**Risiko**: "Model Collapse" (AI-Look verstärkt sich).
**Lösung**: Wir nutzen Prompts, die explizit "Imperfektionen" und "Realismus" fordern (Flux.1 oder Midjourney v6 eignen sich am besten).

## Der "Lena-Marie" Seed-Prompt
Nutze diesen Basis-Prompt, um konsistente Bilder zu generieren. Ändere nur die [Szene] und [Kleidung].

### Basis-Prompt (Englisch für beste Ergebnisse)
> **Subject**: A photo of a 21-year-old German woman, round face, messy dark-blonde bun, wearing tech-glasses, slight freckles, friendly but tired smile.
> **Style**: Shot on 35mm Kodak Portra 400, f/1.8, natural lighting, high texture skin, pores visible, slight film grain, candid shot, authentic look.
> **Negative Prompt** (falls möglich): 3d render, plastic skin, too smooth, heavy makeup, studio lighting, perfect symmetry.

## Generierungs-Liste (20 Bilder Ziel)

### 1. The ID-Sheet (Das Fundament) - 5 Bilder
Generiere Bilder *nur* vom Kopf/Oberkörper vor neutralem Hintergrund, um das Gesicht zu "locken".
- Prompt Add-on: *"Passport photo style, neutral expression, white wall background"*
- Prompt Add-on: *"Looking sideways, laughing, messy hair"*

### 2. DevOps Work Mode - 7-8 Bilder
- Prompt Add-on: *"Sitting at a messy desk with multiple monitors, coding on screen, dark room with monitor glow, focus on face"*
- Prompt Add-on: *"Holding a coffee mug, looking frustrated at laptop, home office"*

### 3. Alpine Outdoor Mode - 7-8 Bilder
- Prompt Add-on: *"Hiking in the bavarian alps, wearing Patagonia fleece jacket, mountains in background, sunny day, wind in hair"*
- Prompt Add-on: *"Selfie angle, holding a pretzel, mountain hut background"*

## Selektions-Prozess (Quality Control)
Bevor du trainierst, sortiere gnadenlos aus:
1. **Hände checken**: Hat sie 5 Finger? Wenn nein -> Löschen oder Inpainting.
2. **Augen checken**: Sind die Pupillen rund?
3. **Plastik-Look**: Sieht die Haut zu glatt aus? -> Löschen. Wir brauchen Textur!

## Nächster Schritt
Speichere die besten 20 Bilder in:
`C:\Users\k4_PC\Projekte\ai_influencer\training_data\synthetic_raw`
