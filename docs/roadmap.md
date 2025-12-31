# Lena-Marie: 2026 Roadmap & Vision 🚀

**Current Status**: ✅ Phase 1 Complete (Autonomous Image/Text Posting, Text DMs).
**Next Phase**: **"Alive & Moving"** (Voice, Video, Perception).

---

## 1. 🎙️ Voice Interaction ("The Voice Upgrade")
**Goal**: Lena should hear and speak, not just read and write.

### A. Hearing (Voice-to-Text)
*   **Technique**: Decode incoming Instagram Voice DMs.
*   **Tech Stack**: **OpenAI Whisper (Local)**.
*   **Implementation**:
    1.  Download audio file from DM (instagrapi supports this).
    2.  Run `whisper` to transcribe to text.
    3.  Feed text to Ollama (Brain).

### B. Speaking (Text-to-Speech)
*   **Technique**: Generate audio replies with a specific, consistent "Lena Voice" (Young, slight German accent, friendly).
*   **Tech Stack Options**:
    *   **ElevenLabs (Cloud)**: Best quality, easiest, costs money (~$5-20/mo).
    *   **Coqui XTTS v2 (Local)**: Free, decent quality, uses VRAM (conflicts with Flux potentially).
*   **Feature**: "Voice Message Sunday" - Users ask questions, she replies via Audio.

---

## 2. 🎥 Video & Reels ("The Motion Upgrade")
**Goal**: Static images are good, but Reels rule the algorithm.

### A. "Talking Head" Stories
*   **Concept**: A 15s Story where Lena talks about her day (Selfie view).
*   **Tech Stack**: **LivePortrait** or **SadTalker**.
*   **Workflow**:
    1.  Generate Flux Image (Selfie).
    2.  Generate Audio (TTS).
    3.  Animate Face via LivePortrait to match Audio.
    *   *Result*: Highly realistic talking video.

### B. Cinematic B-Roll (Atmosphere)
*   **Concept**: Moving shots of the Alps, Coding setups, Walking.
*   **Tech Stack**: **AnimateDiff (ComfyUI)** or **Luma Dream Machine (Cloud)**.
*   **Workflow**:
    1.  Flux Image ("Mountains at sunset").
    2.  Img2Video -> Camera pan, wind moving grass.

---

## 3. 👀 Visual Perception ("The Eyes Upgrade")
**Goal**: Lena should "see" what users send her.

*   **Scenario**: User sends a photo of their PC setup.
*   **Current**: Lena ignores it or says "Nice pic".
*   **Upgrade**: Lena says "Whoa, is that a Keychron keyboard? And nice cable management! 🖥️"
*   **Tech Stack**: **Llava (via Ollama)** or **Llama 3.2 Vision**.
    *   Multimodal LLMs can analyze the image content and describe it to the text-brain.

---

## 4. 🧠 Trend Awareness ("The Zeitgeist Upgrade")
**Goal**: Stop posting random content; post about *Now*.

*   **Concept**: Scraper script that checks:
    *   `#DevOps` trending topics (e.g., "Kubernetes update", "Cloud crash").
    *   `Berlin` events (e.g., "Festival of Lights").
*   **Implementation**:
    *   Feed top news headlines into the `generate_visual_prompt` context.
    *   *Result*: Lena posts: "Everyone talking about the AWS outage today... glad I'm on vacation! 🙈 #aws #devops"

---

## 📅 Proposed Timeline

| Feature | Difficulty | Resource Impact | Priority |
| :--- | :--- | :--- | :--- |
| **Voice Hearing (Whisper)** | ⭐ Easy | Low (Runs on CPU) | High |
| **Visual Perception (Llava)** | ⭐⭐ Medium | High (VRAM) | Medium |
| **Speaking (TTS - Cloud)** | ⭐⭐ Medium | Cost ($) | High |
| **Talking Head Video** | ⭐⭐⭐ Hard | Extreme (VRAM) | Low (Polish) |
| **Reels (B-Roll)** | ⭐⭐⭐ Hard | Extreme (VRAM) | Low |

---

## Suggested Immediate Next Step:
**Implement "Voice Hearing"**.
It allows users to talk to her, which creates a huge "Woah" effect, and Whisper is easy to run locally.
